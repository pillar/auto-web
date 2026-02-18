"""
豆包 (Doubao) Web Driver
基于 Playwright 的自动化驱动
"""
import asyncio
import random
from playwright.async_api import async_playwright, Page, Browser

class DoubaoDriver:
    def __init__(self, headless=False):
        self.headless = headless
        self.browser: Browser = None
        self.page: Page = None
        self.base_url = "https://www.doubao.com"

    async def human_delay(self, min_s=0.5, max_s=1.5):
        """模拟人类延迟"""
        await asyncio.sleep(random.uniform(min_s, max_s))
    
    async def start(self):
        """启动浏览器并打开豆包"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        await self.page.goto(self.base_url)
        print("[Doubao] 已打开页面，请手动登录...")
        return self
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    # ============ Skill Runner 接口 ============
    
    async def click(self, selector: str, timeout: int = 5000):
        """拟人化点击（带延迟和 hover）"""
        print(f"[Driver] 准备点击: {selector}")
        await self.human_delay(0.5, 1.5)
        
        # 先 hover（模拟鼠标移动过去）
        try:
            await self.page.locator(selector).first.hover()
            await self.human_delay(0.2, 0.5)
        except:
            pass
            
        await self.page.locator(selector).first.click(timeout=timeout)
    
    async def fill(self, text: str, clear: bool = True):
        """拟人化输入（带延迟）"""
        print(f"[Driver] 拟人化输入 ({len(text)} 字符)...")
        await self.human_delay(1.0, 2.0)
        
        # 定位输入框
        input_selector = "div[contenteditable='true']"
        textarea_selector = "textarea"
        
        try:
            # 优先尝试 contenteditable
            input_box = self.page.locator(input_selector).first
            if await input_box.count() > 0:
                elem = input_box
            else:
                elem = self.page.locator(textarea_selector).first
            
            # 聚焦并清空
            await elem.click()
            await self.human_delay(0.2, 0.5)
            if clear:
                await elem.fill("")
            
            # 打字机效果（每个字间隔 30-80ms 随机）
            # 对于长文本，press_sequentially 还是太慢，容易被认为是不自然
            # 折中：快速打字 (delay=20ms)
            await elem.press_sequentially(text, delay=20)
            
        except Exception as e:
            print(f"[Driver] 填词失败: {e}")
            raise
    
    async def wait_for(self, selector: str, timeout: int = 10000):
        """等待元素出现"""
        print(f"[Driver] 等待元素: {selector}")
        await self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
        return self.page.locator(selector).first
    
    async def press_enter(self):
        """拟人化回车（带延迟）"""
        print("[Driver] 准备发送...")
        await self.human_delay(0.5, 1.0)
        await self.page.keyboard.press("Enter")
    
    async def click_send_button(self):
        """点击发送按钮"""
        send_btn = self.page.locator("button:has-text('发送'), button.send-btn, [data-testid='send-button']").first
        if await send_btn.count() > 0:
            await send_btn.click()
            print("[Driver] 点击发送按钮")
        else:
            await self.press_enter()
    
    # ============ 高级方法 ============
    
    async def screenshot(self, path: str = None):
        """截图"""
        if path is None:
            path = f"screenshot_{asyncio.get_event_loop().time()}.png"
        await self.page.screenshot(path=path)
        print(f"[Driver] 截图保存: {path}")
        return path
    
    async def get_text(self, selector: str) -> str:
        """获取元素文本"""
        elem = self.page.locator(selector).first
        return await elem.inner_text()
    
    async def scroll_to_bottom(self):
        """滚动到页面底部"""
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")


# 同步封装（方便简单调用）
class DoubaoDriverSync:
    def __init__(self, headless=False):
        self.driver = DoubaoDriver(headless=headless)
        self.loop = asyncio.new_event_loop()
    
    def start(self):
        return self.loop.run_until_complete(self.driver.start())
    
    def close(self):
        return self.loop.run_until_complete(self.driver.close())
    
    def run_skill(self, runner, skill_name, **vars):
        """同步方式运行 skill"""
        return self.loop.run_until_complete(runner.run(skill_name, **vars))
