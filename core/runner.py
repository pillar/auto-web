import asyncio
import os
import json
import sys
from playwright.async_api import async_playwright

# 路径配置
BASE_DIR = "/Users/pillar/clawd/auto-web"
SESSION_ROOT = os.path.join(BASE_DIR, "sessions")
DRIVERS_DIR = os.path.join(BASE_DIR, "drivers")

async def run_task(platform, message, headless=True):
    session_dir = os.path.join(SESSION_ROOT, platform)
    driver_js_path = os.path.join(DRIVERS_DIR, f"{platform}.js")
    
    if not os.path.exists(session_dir):
        print(f"[!] Error: Session for {platform} not found. Run setup_session.py first.")
        return
    
    if not os.path.exists(driver_js_path):
        print(f"[!] Error: Driver for {platform} not found.")
        return

    with open(driver_js_path, 'r') as f:
        driver_js = f.read()

    async with async_playwright() as p:
        print(f"[*] Launching persistent context for {platform}...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 定义目标 URL
        urls = {
            "xyq": "https://xyq.jianying.com/",
            "doubao": "https://www.doubao.com/chat/",
            "gemini": "https://gemini.google.com/app"
        }
        target_url = urls.get(platform)
        
        print(f"[*] Navigating to {target_url}...")
        await page.goto(target_url, wait_until="networkidle")
        
        # 针对不同平台的预处理（例如：小云雀需要点“开始创作”）
        if platform == "xyq":
            print("[*] Checking for Start button...")
            start_btn = page.locator('button:has-text("开始创作"), .generate-btn').first
            try:
                await start_btn.wait_for(state="visible", timeout=5000)
                await start_btn.click()
                print("[*] Start button clicked.")
                await asyncio.sleep(2)
            except:
                print("[*] Start button not found or already in editor.")

        print(f"[*] Injecting driver and sending prompt: {message[:20]}...")
        
        # 注入并执行
        result = await page.evaluate(f"""
            async (msg) => {{
                {driver_js}
                try {{
                    return await window.autoWeb_{platform}.sendPrompt(msg);
                }} catch (e) {{
                    return {{ error: e.message }};
                }}
            }}
        """, message)
        
        print(f"[+] Task Result: {json.dumps(result, ensure_ascii=False)}")
        
        # 保持片刻观察结果（如果是无头模式其实看不见，但逻辑上建议等待）
        await asyncio.sleep(3)
        await context.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python runner.py <platform> <message>")
        sys.exit(1)
        
    platform = sys.argv[1]
    message = sys.argv[2]
    # 默认 Headless=False 方便 Boss 观察，稳定后可改为 True
    asyncio.run(run_task(platform, message, headless=False))
