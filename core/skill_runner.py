import yaml
import re
from pathlib import Path

class SkillRunner:
    def __init__(self, driver):
        self.driver = driver
        # 修改：从 core/skills 改为项目根目录下的 skills
        self.skills_dir = Path(__file__).parent.parent / "skills"
    
    def load(self, skill_name):
        """加载 skill 配置"""
        skill_path = self.skills_dir / f"{skill_name}.yaml"
        if not skill_path.exists():
            raise FileNotFoundError(f"Skill not found: {skill_name}")
        
        with open(skill_path) as f:
            return yaml.safe_load(f)
    
    def render_prompt(self, template, vars_dict):
        """渲染 prompt 模板，支持 {{var}} 和 {{var|default}}"""
        def replacer(match):
            content = match.group(1)
            if '|' in content:
                var, default = content.split('|', 1)
                var = var.strip()
                default = default.strip().strip("'\"")
                return str(vars_dict.get(var, default))
            return str(vars_dict.get(content, ''))
        
        return re.sub(r'\{\{([^}]+)\}\}', replacer, template)
    
    async def run(self, skill_name, **vars):
        """执行 skill"""
        config = self.load(skill_name)
        
        # 1. 激活模式
        if 'activate' in config:
            activate_cfg = config['activate']
            
            # 多步激活（如 Seedance 需要先点图像生成，再点 Seedance）
            if 'steps' in activate_cfg:
                for i, step in enumerate(activate_cfg['steps']):
                    print(f"[Skill] 激活步骤 {i+1}: {step['selector']}")
                    if step.get('selector'):
                        await self.driver.click(step['selector'])
                    if step.get('wait_for'):
                        await self.driver.wait_for(
                            step['wait_for'], 
                            timeout=step.get('timeout', 5000)
                        )
            # 单步激活
            elif activate_cfg.get('selector'):
                print(f"[Skill] 激活模式: {activate_cfg['selector']}")
                await self.driver.click(activate_cfg['selector'])
                await self.driver.wait_for(
                    activate_cfg['wait_for'], 
                    timeout=activate_cfg.get('timeout', 5000)
                )
            else:
                # 无特定模式，只等待输入框
                if activate_cfg.get('wait_for'):
                    await self.driver.wait_for(
                        activate_cfg['wait_for'],
                        timeout=activate_cfg.get('timeout', 5000)
                    )
        
        # 2. 渲染并填写 prompt
        prompt = self.render_prompt(config['prompt'], vars)
        print(f"[Skill] Prompt: {prompt[:100]}...")
        await self.driver.fill(prompt)
        
        # 3. 提交生成
        if 'submit' in config:
            submit_cfg = config['submit']
            selector = submit_cfg.get('selector')
            
            if selector:
                print(f"[Skill] 点击生成按钮...")
                await self.driver.click(selector)
            else:
                # 无特定按钮，按回车发送
                print(f"[Skill] 按回车发送...")
                await self.driver.press_enter()
            
            if submit_cfg.get('wait_result'):
                result = await self.driver.wait_for(
                    submit_cfg['wait_result'],
                    timeout=submit_cfg.get('timeout', 60000)
                )
                print(f"[Skill] 生成完成!")
                return result

# 使用示例
# runner = SkillRunner(doubao_driver)
# await runner.run("xiaohongshu-cover", topic="夏日穿搭", style="日系清新")
