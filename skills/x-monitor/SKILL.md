# Skill: X Expert Monitor

## Description
Periodically checks the profiles of selected X/Twitter experts for new high-value posts using the browser tool.

## Monitored List
- @FuSheng_0306 (OpenClaw Insights)
- @karry_viber (Agent Architecture)
- @JamesAI (Skill Automation)

## Workflow
1. Navigate to `https://x.com/<username>`.
2. Take a snapshot/screenshot of the latest tweets.
3. Compare with the last known "top tweet ID" stored in `memory/x-monitor-state.json`.
4. If new content exists:
   - Extract the text.
   - Summarize.
   - Save to `research/X-inbox/`.
   - Notify the user via the current channel.
