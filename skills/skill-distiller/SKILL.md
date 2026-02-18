# Skill: Skill Distiller

## Description
Automates the "JamesAI Workflow" of turning raw methodology (Markdown files) into executable OpenClaw Skills.

## Workflow
1. Input: A Markdown file in `research/X-inbox/`.
2. Step 1: Analyze the source for "Methodology", "Triggers", "Steps", and "Parameters".
3. Step 2: Generate a standard `SKILL.md` file in `skills/<skill-name>/`.
4. Step 3: (Optional) Scaffold placeholder Python/Bash scripts for automation if the methodology describes a toolable process.
5. Step 4: Register the new skill in the session's context.

## Trigger
- "提炼这个素材为 Skill"
- "把 [文件名] 封装成我的能力"
