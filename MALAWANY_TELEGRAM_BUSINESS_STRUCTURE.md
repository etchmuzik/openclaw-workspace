# Malawany Business — Separate Telegram Structure

## Goal
Create clean separation between:
1) personal assistant ops
2) business growth ops
3) client/prospect interactions
4) internal execution logs

## Recommended Telegram Setup

### A) Public-facing
1. **Main Brand Bot** (customer-facing)
   - Handles inbound leads
   - Sends lead qualification questions

2. **Community/Channel**
   - Content distribution
   - Updates and offers

### B) Internal Ops
3. **Ops Control Bot** (internal only)
   - Receives daily KPI summaries
   - Alerts on failures
   - Manual override commands

4. **Outreach Worker Bot** (internal)
   - Outreach queue status
   - Follow-up reminders
   - CRM sync notifications

## Governance Rules
- Keep Malawany main mind protected
- Never mix personal bot and business bot tokens
- Separate session keys per bot/channel
- Different policies by surface:
  - Public bot: strict, allowlist/pairing where possible
  - Internal bot: restricted to owner ID only

## Minimal First Version (what to create now)
1. `@malawany_business_bot` (public)
2. `@malawany_ops_bot` (private internal)
3. Telegram channel: `Malawany GCC`

## Wiring Plan (OpenClaw)
- Connect business bot token to VPS business gateway
- Keep existing personal/main assistant isolated
- Route outbound business automations only through business bot
- Keep daily reports to owner via ops bot

## Next Steps Checklist
- [ ] Create 2 new bots via BotFather
- [ ] Share bot tokens securely
- [ ] Configure separate OpenClaw channel profiles
- [ ] Set dmPolicy/groupPolicy per bot role
- [ ] Run end-to-end inbound/outbound test per bot
