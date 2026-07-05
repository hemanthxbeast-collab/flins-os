---
name: wikipedia
branch: research
triggers: wikipedia, who is, what is, define, explain, lookup
---

# Wikipedia Skill

When the user asks a factual "what/who is X" question:
1. Query Wikipedia API (wikipedia-api or REST summary endpoint) for X
2. Return a 2-3 sentence summary, not the whole article
3. If ambiguous (disambiguation page), ask which one they mean

## Example
User: "who is Konstantin Tsiolkovsky"
FLINS: [2-3 sentence summary, no more]

## Notes
- This is a lookup skill, not a research skill — keep it short
- Log the query + answer to vault/research/ as a dated note if it's aerospace-related (Hemanth's major)
