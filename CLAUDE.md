# Project Context: Auto-Web (Musk-Lean)

## 🎯 Goal
Automated web interaction library using Agent-driven selector caching. High performance, zero-fluff, token-efficient.

## 🧠 Protocol (3-Layer Memory)
1. **L1 (Project)**: This `CLAUDE.md`.
2. **L2 (Operational)**: `drivers/*.json` (Cached Selectors).
3. **L3 (History)**: `docs/logs/*.md` (Site change post-mortems).

## 📋 Rules
- **Selector First**: Never re-parse DOM if a selector exists in `drivers/`.
- **Hybrid execution**: Agent decides *what* to do; pre-written JS handles *how*.
- **Token Efficiency**: Only request accessibility tree snapshots if selectors fail.
- **Resilience**: If a selector fails, auto-trigger "Explore Mode" to find the new one and update the JSON.

## 🏗️ Architecture
- `/core`: Logic to connect with OpenClaw browser/CDP.
- `/drivers`: Per-platform JS drivers and JSON selector maps.
- `/docs/decisions`: Post-mortems for UI breaking changes.
