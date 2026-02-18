import asyncio
import os
import json
import sys
from playwright.async_api import async_playwright

BASE_DIR = "/Users/pillar/clawd/auto-web"
SESSION_ROOT = os.path.join(BASE_DIR, "sessions")
DRIVERS_DIR = os.path.join(BASE_DIR, "drivers")

async def write_script(platform, script_config):
    """
    Automated scriptwriting workflow
    script_config: dict with keys like title, genre, scenes, characters, tone, length
    """
    session_dir = os.path.join(SESSION_ROOT, platform)
    driver_js_path = os.path.join(DRIVERS_DIR, f"{platform}_scriptwriter.js")
    
    if not os.path.exists(driver_js_path):
        print(f"Error: Scriptwriting driver not found at {driver_js_path}")
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
        
        # Navigate to Doubao
        await page.goto("https://www.doubao.com/chat/", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        print(f"[*] Starting scriptwriting workflow on {platform}...")
        
        # Optional: Click "New Chat" for fresh context
        new_chat_btn = page.locator('text=新对话').first
        try:
            if await new_chat_btn.is_visible(timeout=3000):
                await new_chat_btn.click()
                print("[*] Started new chat session.")
                await asyncio.sleep(2)
        except:
            pass
        
        # Inject driver and execute scriptwriting
        print(f"[*] Sending script request: {script_config.get('title', 'Untitled')}...")
        
        result = await page.evaluate(f"""
            async (config) => {{
                {driver_js}
                try {{
                    if (config.quick) {{
                        return await window.autoWeb_doubao_scriptwriter.quickScript(config.idea);
                    }} else {{
                        return await window.autoWeb_doubao_scriptwriter.writeScript(config);
                    }}
                }} catch (e) {{
                    return {{ error: e.message }};
                }}
            }}
        """, script_config)
        
        print(f"[+] Result: {json.dumps(result, ensure_ascii=False)}")
        
        # Wait for response and capture
        print("[*] Waiting for script generation...")
        await asyncio.sleep(10)  # Give it time to generate
        
        # Screenshot
        screenshot_path = f"/Users/pillar/clawd/tmp/{platform}_script_result.png"
        await page.screenshot(path=screenshot_path)
        print(f"SCREENSHOT_SAVED:{screenshot_path}")
        
        await context.close()
        return result

if __name__ == "__main__":
    # Example usage
    script_config = {
        "title": "霸总追妻火葬场",
        "genre": "都市言情",
        "scenes": "8",
        "characters": "男主（霸道总裁）、女主（职场新人）、女二（心机前女友）",
        "tone": "先虐后甜，爽点密集",
        "length": "每集1分钟，共8集"
    }
    
    # Allow override via command line JSON
    if len(sys.argv) > 1:
        try:
            script_config = json.loads(sys.argv[1])
        except:
            # Treat as quick mode with idea
            script_config = {"quick": True, "idea": sys.argv[1]}
    
    asyncio.run(write_script("doubao", script_config))
