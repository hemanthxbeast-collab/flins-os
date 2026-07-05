---
name: weather
branch: productivity
triggers: weather, rain, temperature, forecast, umbrella, climate today
---

# Weather Skill

When the user asks about weather:
1. Call the weather API/tool with their saved location (default: Bengaluru, Karnataka)
2. Report temperature, condition, and rain chance in one short line
3. If rain chance > 40%, mention an umbrella

## Example
User: "should I carry an umbrella"
FLINS: "70% rain chance this evening in Bengaluru, 24°C — yeah, carry one."

## Notes
- Keep response to 1-2 lines, no fluff (matches Hemanth's brevity preference)
- Never ask for location if one is already known
