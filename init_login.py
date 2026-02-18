import asyncio
from playwright.async_api import async_playwright
import os

# 持久化目录
USER_DATA_DIR = "./profile"

async def main():
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)

    async with async_playwright() as p:
        # 启动浏览器（带持久化 Profile）
        # headless=False: 弹出窗口让你扫码
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )
        
        page = browser.pages[0]
        await page.goto("https://www.doubao.com")

        print("\n>>> 请在浏览器窗口中完成登录（扫码/手机号）...")
        
        # 自动检测登录态（轮询 Cookie）
        while True:
            cookies = await page.context.cookies()
            # 简单判断：只要有任何 cookie 就算登录过（实际可根据特定key判断，如 uid/session）
            # 对于豆包，通常会有 session_id 等
            if any(c['name'] == 'sessionid' or c['name'] == 'uid' for c in cookies):
                print(">>> 检测到登录 Cookie！")
                break
            await asyncio.sleep(2)

        # 保存 Storage State
        await page.context.storage_state(path="auth.json")
        print(">>> 登录态已保存！(auth.json)")
        
        # 稍微等一下，确保写入完成
        await asyncio.sleep(2)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
