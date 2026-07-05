---
name: email
branch: communication
triggers: email, mail, inbox, send message, draft mail, reply to
---

# Email Skill

When the user asks to check, draft, or send email:
1. If reading: fetch unread/recent via IMAP (local creds from .env, never hardcode)
2. If drafting: ask ONLY for recipient + intent if not given, then write it directly — no back and forth
3. If sending: confirm once before actually sending ("send this to X? y/n")

## Example
User: "flins draft a mail to Nishanth about the chem project deadline"
FLINS: [drafts mail, shows it, waits for confirm before sending]

## Notes
- SMTP/IMAP creds live in .env — never print them back to the user or logs
- Keep drafts short and direct, match Hemanth's own writing style (casual, to the point)
