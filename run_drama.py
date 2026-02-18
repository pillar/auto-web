import asyncio
from playwright.async_api import async_playwright
from drivers.doubao import DoubaoDriver
from core.skill_runner import SkillRunner

async def main():
    # 1. 启动浏览器（加载持久化 Profile 和登录态）
    USER_DATA_DIR = "./profile"
    
    async with async_playwright() as p:
        print(f">>> 启动浏览器 (Profile: {USER_DATA_DIR})...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )
        
        page = context.pages[0]
        await page.goto("https://www.doubao.com")
        
        # 等待页面稳定
        print(">>> 等待 5 秒让页面稳定...")
        await asyncio.sleep(5)
        
        # 注入 page 到 driver
        driver = DoubaoDriver(headless=False)
        driver.page = page
        driver.browser = context  # 保持引用防止关闭
        
        runner = SkillRunner(driver)

        try:
            # 2. 执行短剧创作 Skill
            print(">>> 开始执行短剧创作 Skill (全自动模式)...")
            await runner.run(
                "short-drama-script",
                genre="末日生存+外卖骑手",
                roles="男主：外卖骑手（跑腿王，对路线极熟）；反派：泄露消息的神秘生物公司高管",
                conflict="送餐时偶然听到僵尸入侵倒计时，没人信，只能利用送外卖的优势开始疯狂囤货和改造",
                twist="原本被看不起的骑手，在末日成了唯一能连接各据点的英雄，最终发现僵尸病毒解药竟然在外卖箱的保温层里...",
                extra_requirements="一共30集，每集1分钟。要求：\n1. 每集开头必须有'黄金3秒'视觉冲击。\n2. 结尾必须有钩子。\n3. 结合抖音热点（如'科目三'躲僵尸、'特种兵旅游'式逃亡）。"
            )
            print("\n>>> ✅ Skill 执行完成！")
        except Exception as e:
            print(f"\n>>> ❌ Skill 执行出错: {e}")
            import traceback
            traceback.print_exc()
            print(">>> ⚠️ 浏览器将保持打开，方便你调试...")

        # 3. 保持浏览器打开
        print("\n>>> 浏览器保持运行中。按 Ctrl+C 退出。")
        # 无限循环防止退出
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
