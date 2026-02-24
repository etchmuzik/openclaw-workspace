# Hostinger OpenClaw One-Click Runbook

Last updated: 2026-02-24
Owner policy: **Do not change Malawany runtime/config unless Etch explicitly asks.**

---

## 0) Scope

This runbook is for deploying OpenClaw on **Hostinger VPS** using **Docker Manager one-click** and then hardening it.

---

## 1) One-click deploy (hPanel)

1. Open **hPanel → VPS → Docker Manager**.
2. Go to **Catalog**.
3. Search for **OpenClaw**.
4. Click **Deploy**.
5. In env vars, keep/save:
   - `OPENCLAW_GATEWAY_TOKEN` (required)
   - Optional API keys: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `XAI_API_KEY`
6. Confirm deployment and wait for status: **Running**.
7. Open mapped port in browser: `http://<VPS_IP>:<PORT>`.
8. Login with `OPENCLAW_GATEWAY_TOKEN`.

---

## 2) Immediate post-deploy security

Do these right away:

- [ ] Store gateway token in a secure vault (not plain chat/text files).
- [ ] Rotate token if exposed.
- [ ] Restrict inbound ports in firewall to only required ports.
- [ ] Prefer private access (SSH tunnel or tailnet) over public exposure.
- [ ] Run security checks:

```bash
openclaw doctor
openclaw security audit
openclaw security audit --deep
```

---

## 3) Validate health

From VPS shell:

```bash
openclaw status
openclaw gateway status
```

Expected:
- Gateway: running
- Web login accepts token
- Channel pages accessible (if configured)

---

## 4) Backup policy

Backup these paths regularly:

- `~/.openclaw/`
- `~/.openclaw/workspace/`

Minimum cadence:
- daily incremental
- weekly full snapshot

Before upgrades:
- forced backup + restore test on a second VM (or local test path)

---

## 5) Updating safely

In Docker Manager:
1. Open project
2. Pull/update image
3. Restart container
4. Re-check:

```bash
openclaw doctor
openclaw security audit
openclaw gateway status
```

---

## 6) Common issues + fixes

### A) Can’t log in to Control UI
- Verify token is correct (`OPENCLAW_GATEWAY_TOKEN`)
- Confirm correct URL/port
- Check container logs in Docker Manager

### B) Container starts then exits
- Missing/invalid env vars
- Port collision
- Corrupt persistent state (restore backup)

### C) WhatsApp QR / channel issue
- Reopen channel page and regenerate QR
- Restart container once
- Recheck logs for auth/session errors

### D) Slow or unstable behavior
- Upgrade VPS plan/resources
- Reduce heavy concurrent tasks
- Check memory/CPU pressure in host metrics

---

## 7) Bot ownership map (locked)

- **Malawany**: main mind (locked; no changes without explicit Etch approval)
- **@etchclawdbot**: VPS ops/gateway bot
- **@Etch_vps_bot (H1)**: secondary VPS checks

Status reporting format (recommended):
1 line per bot, no mixing.

---

## 8) Quick command block (copy/paste)

```bash
openclaw status
openclaw gateway status
openclaw doctor
openclaw security audit
```

---

## 9) Reference links

Official:
- https://docs.openclaw.ai/vps
- https://docs.openclaw.ai/install
- https://docs.openclaw.ai/gateway/security
- https://docs.openclaw.ai/help/environment

Hostinger:
- https://www.hostinger.com/vps/docker/openclaw
- https://www.hostinger.com/support/how-to-install-openclaw-on-hostinger-vps/
- https://www.hostinger.com/tutorials/how-to-set-up-openclaw
