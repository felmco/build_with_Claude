# 5.6 Security Best Practices

## 1. Prompt Injection
Users trying to override your instructions ("Ignore previous instructions...").
- **Defense:** Separate data from instructions.
- **Defense:** Use XML tags (`<user_input>`).

## 2. PII Leaks
Don't send sensitive data (SSN, Credit Cards) to the API unless you have a BAA/Enterprise agreement covering it.
- **Scrubbing:** Remove PII before sending.

## 3. Key Management
- Never commit keys to Git.
- Use `.env`.
- Rotate keys if leaked.

## Next Steps
- [Compliance](./22_compliance.md).
