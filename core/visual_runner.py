import asyncio
import os
import json
import sys
from playwright.async_api import async_playwright

BASE_DIR = "/Users/pillar/clawd/auto-web"
SESSION_ROOT = os.path.join(BASE_DIR, "sessions")
DRIVERS_DIR = os.path.join(BASE_DIR, "drivers")

async def run_and_capture(platform, message):
    session_dir = os.path.join(SESSION_ROOT, platform)
    driver_js_path = os.path.join(DRIVERS_DIR, f"{platform}.js")
    
    if not os.path.exists(driver_js_path):
        print(f"Error: Driver {driver_js_path} not found")
        return

    with open(driver_js_path, 'r') as f:
        driver_js = f.read()

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        urls = {
            "doubao": "https://www.doubao.com/chat/",
            "gemini": "https://gemini.google.com/app",
            "xyq": "https://xyq.jianying.com/"
        }
        print(f"[*] Navigating to {urls[platform]}...")
        try:
            await page.goto(urls[platform], wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000) # Give it some breathing room
        except Exception as e:
            print(f"[!] Navigation warning: {e}")
        
        # Optional pre-action for specific platforms
        if platform == "xyq":
             start_btn = page.locator('button:has-text("开始创作"), .generate-btn').first
             try:
                 await start_btn.wait_for(state="visible", timeout=5000)
                 await start_btn.click()
                 await asyncio.sleep(2)
             except: pass
        
        if platform == "doubao":
             print("[*] Ensuring fresh chat for Doubao...")
             # Look for "New Chat" text or similar icon
             new_chat_btn = page.locator('text=新对话').first
             try:
                 if await new_chat_btn.is_visible(timeout=3000):
                     await new_chat_btn.click()
                     print("[*] Clicked New Chat.")
                     await asyncio.sleep(2)
             except:
                 print("[*] New Chat button not found, assuming already in a conversation.")

        print(f"[*] Injecting {platform} driver and sending: {message[:30]}...")
        
        # Inject and Send
        result = await page.evaluate(f"""
            async (msg) => {{
                {driver_js}
                return await window.autoWeb_{platform}.sendPrompt(msg);
            }}
        """, message)
        
        print(f"[+] Driver Result: {json.dumps(result, ensure_ascii=False)}")
        
        # Wait for response UI
        await asyncio.sleep(5)
        
        screenshot_path = f"/Users/pillar/clawd/tmp/{platform}_result.png"
        await page.screenshot(path=screenshot_path)
        print(f"SCREENSHOT_SAVED:{screenshot_path}")
        
        await context.close()

if __name__ == "__main__":
    p = sys.argv[1]
    m = sys.argv[2]
    asyncio.run(run_and_capture(p, m))
