# Skill: Spatialized Context Manager

## Description
Implements the "4-zone 11-channel" logic from Discord into a single-session environment like WhatsApp. Uses labels and `#` prefixes to hot-swap personalities, memory contexts, and system prompts.

## Files
- `SPACES.md`: The registry of available spaces.
- `AGENTS.md`: Rules for switching.

## Logic
1. Detect `#command` at the start of a message.
2. Cross-reference `SPACES.md` for the corresponding persona and context.
3. Apply `session_status` label for tracking.
4. Prepend the space's specific instructions to the current turn's system prompt.
