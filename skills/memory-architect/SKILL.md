# Skill: Memory Architect

## Description
Implements the 3-layer memory architecture (Logs, Long-term, Buffer) to ensure the Agent gets smarter over time and never loses track of long-running tasks.

## Workflow
1. **Durable Logging**: Every major interaction is logged to `memory/YYYY-MM-DD.md`.
2. **Knowledge Compounding**: Regularly distill logs into `MEMORY.md`.
3. **State Buffering**: Use `SESSION-STATE.md` for active complex tasks to survive context window compression.
4. **Janitorial Duties**: Move old P1/P2 memories to `memory/archive/`.

## Commands
- "执行记忆提炼": Triggers log-to-memory distillation.
- "清理过期记忆": Triggers the janitor script.
- "更新任务状态": Manually sync current progress to `SESSION-STATE.md`.

## Automation
- A nightly Cron job runs `scripts/memory_janitor.py` and `scripts/knowledge_compounding.py`.
