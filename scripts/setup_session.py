import asyncio
import os
import sys
from playwright.async_api import async_playwright

SESSION_ROOT = "/Users/pillar/clawd/auto-web/sessions"

async def setup_session(platform):
    platform_dir = os.path.join(SESSION_ROOT, platform)
    os.makedirs(platform_dir, exist_ok=True)
    
    urls = {
        "doubao": "https://www.doubao.com/chat/",
        "gemini": "https://gemini.google.com/app",
        "xyq": "https://xyq.jianying.com/"
    }
    url = urls.get(platform, "https://google.com")
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=platform_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = await context.new_page()
        print(f"[*] Opening {platform} at {url}...")
        await page.goto(url)
        
        print("\n" + "="*50)
        print(f"正在进行 [{platform}] 的身份初始化")
        print("请在弹出的浏览器窗口中手动完成登录。")
        print("登录成功并看到主界面后，请直接关闭该浏览器窗口。")
        print("="*50 + "\n")
        
        while True:
            try:
                if page.is_closed():
                    break
            except:
                break
            await asyncio.sleep(1)
            
        await context.close()
        print(f"[*] Session for {platform} saved.")

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "doubao"
    asyncio.run(setup_session(p))
