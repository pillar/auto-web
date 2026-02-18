import asyncio
import os
from playwright.async_api import async_playwright

SESSION_DIR = "/Users/pillar/clawd/auto-web/sessions/xyq"

async def debug_xyq():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False
        )
        page = await context.new_page()
        await page.goto("https://xyq.jianying.com/")
        
        # 1. Click Start
        start_btn = page.locator('button:has-text("开始创作"), .generate-btn').first
        await start_btn.click()
        await asyncio.sleep(2)
        
        # 2. Enter test text
        input_area = page.locator('textarea, [contenteditable="true"]').first
        await input_area.fill("Debug prompt")
        await asyncio.sleep(1)
        
        # 3. Take snapshot of all buttons
        buttons = await page.eval_on_selector_all("button, [role='button'], .generate-btn", 
            "els => els.map(el => ({ text: el.innerText, class: el.className, id: el.id, visible: el.offsetParent !== null }))")
        
        print("DEBUG_BUTTONS:" + str(buttons))
        
        # 4. Screenshot for visual confirmation
        await page.screenshot(path="/Users/pillar/clawd/tmp/xyq_debug_buttons.png")
        await context.close()

if __name__ == "__main__":
    asyncio.run(debug_xyq())
