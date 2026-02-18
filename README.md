# Auto-Web

Automated web interaction library designed for AI Agents.

## Concept: Selector Caching
Instead of reading the whole DOM tree every time, we use "Platform Drivers".
1. **L1**: JSON Selectors (The "Where").
2. **L2**: JS Logic (The "How").

## Workflow
1. Agent checks `drivers/platform.json`.
2. If selectors found, inject `drivers/platform.js`.
3. If fails (UI updated), Agent runs `browser snapshot` to find new selectors and updates JSON.

## Platforms
- [x] Doubao (Concept)
- [ ] Gemini (WIP)
- [ ] Jimeng (WIP)
