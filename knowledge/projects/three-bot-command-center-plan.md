# Three-Bot Command Center Plan

Date: 2026-02-24
Owner: Etch

## Bot Roles (locked)
1. @malawany_bot — Main mind (protected, no config/runtime changes without explicit Etch approval)
2. @Etch_vps_bot (H1) — VPS ops/worker bot
3. @etchclawdbot — New VPS bot (47033 stack)

## Command Center Scope
Single mission control view with per-bot health, ownership, and action lane separation.

## Control Rules
- Never mix personal/main mind actions with worker actions.
- Every status report is split by bot (1 line each minimum).
- Group behavior: reply only when mentioned (where configured).

## Operational Plan

### Layer 1 — Health (every cycle)
- Check gateway reachability
- Check Telegram channel state
- Check WhatsApp state (where enabled)
- Detect polling conflicts (Telegram 409)

### Layer 2 — Work Allocation
- Malawany: strategy, verification, approvals
- H1: VPS ops execution + infra checks
- etchclawdbot: growth/business automations

### Layer 3 — Recovery Playbooks
- If Telegram inbound fails: detect 409 conflict -> identify duplicate poller -> rotate/rebind token if needed
- If model auth fails: verify provider auth profile in that exact instance/container
- If channel offline: restart service, validate logs, run outbound/inbound test

## KPIs (dashboard targets)
- Bot uptime per bot
- Inbound response success
- Outbound delivery success
- Mean time to recover (MTTR)

## Immediate Actions
- [ ] Add explicit per-bot heartbeat widgets to mission-control
- [ ] Add one-click tests: Telegram outbound, inbound probe note, WhatsApp outbound
- [ ] Add incident timeline panel for each bot
- [ ] Lock production policies after testing phase

## Reporting Format (fixed)
- Malawany: [status] [notes]
- H1: [status] [notes]
- etchclawdbot: [status] [notes]