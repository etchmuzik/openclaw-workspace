# OpenClaw VPS Knowledge Pack (Malawany)

Last updated: 2026-02-24
Owner note: **Malawany is locked (main mind). Do not modify Malawany runtime/config without explicit approval from Etch.**

---

## 1) OpenClaw fundamentals (operator view)

- OpenClaw runs as a **Gateway daemon** plus agent sessions/tools.
- In VPS deployments, the VPS Gateway is the source of truth for state/workspace.
- Keep trust boundaries clear: one trusted operator boundary per gateway.

### Essential commands

```bash
openclaw status
openclaw gateway status
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw doctor
openclaw dashboard
openclaw security audit
openclaw security audit --deep
```

---

## 2) Install on VPS (recommended baseline)

## Hostinger one-click deploy (focus)

If you want fastest deployment on Hostinger:

1. In hPanel, open **Docker Manager**.
2. Go to **Catalog** and select **OpenClaw**.
3. Click **Deploy**.
4. Save the generated `OPENCLAW_GATEWAY_TOKEN` securely.
5. (Optional) Add provider keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, etc.) during deploy or later.
6. Wait until container status is **Running**.
7. Open the mapped web port (`http://your-vps-ip:port`) and log in with the gateway token.

If you do not have a VPS yet, you can start from Hostinger’s OpenClaw VPS page and deploy with the preconfigured template.

### Hostinger hardening after one-click (required)

- Immediately rotate/replace any default or auto-generated weak secrets.
- Restrict public exposure where possible (prefer private access via tunnel/tailnet).
- Run `openclaw security audit` after first boot and after each network/config change.
- Back up `~/.openclaw` + workspace.

## Preferred method (official installer)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Install only, skip onboarding:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

## Alternative npm path

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

## Verify

```bash
openclaw doctor
openclaw status
openclaw gateway status
```

---

## 3) VPS security baseline (must-have)

1. Use a clean Ubuntu/Debian base image.
2. Prefer loopback binding + private access (SSH tunnel or Tailscale).
3. If binding to LAN/tailnet, require gateway auth token/password.
4. Run regular audits:

```bash
openclaw security audit
```

5. Keep business/shared agents isolated from personal profiles/accounts.
6. Back up `~/.openclaw` and workspace regularly.

---

## 4) Access patterns

### Safest default
- Gateway bound privately (loopback)
- Access via:
  - SSH tunnel (`ssh -L ...`), or
  - Tailscale private network / serve

### If exposed wider
- Enforce strong token/password auth
- Restrict allowed senders/channels
- Re-run security audit after every config/network change

---

## 5) Environment variables to know

- `OPENCLAW_HOME` — override home for internal path resolution
- `OPENCLAW_STATE_DIR` — override state dir (default `~/.openclaw`)
- `OPENCLAW_CONFIG_PATH` — override config file path
- `OPENCLAW_LOG_LEVEL` — runtime log level override

Env precedence (high → low):
1) Process env
2) local `.env`
3) global `~/.openclaw/.env`
4) config `env` block
5) optional shell-env import

(Values are non-overriding by design.)

---

## 6) Provider options (official docs)

- Railway
- Northflank
- Oracle Cloud (Always Free)
- Fly.io
- Hetzner (Docker)
- GCP
- exe.dev
- AWS (supported pattern)

---

## 7) Quick deployment checklist (VPS)

- [ ] Provision clean VPS
- [ ] Install OpenClaw via installer script
- [ ] Complete onboarding with daemon install
- [ ] Set auth token/password
- [ ] Keep gateway private (loopback + tunnel/tailnet) if possible
- [ ] Run `openclaw doctor`
- [ ] Run `openclaw security audit`
- [ ] Configure backups for state/workspace
- [ ] Validate channel routing + dry-run checks

---

## 8) Your bot assignment policy (Etch)

- **Malawany**: main mind, locked
  - No config/runtime changes unless Etch explicitly requests
- **@etchclawdbot**: VPS gateway/ops bot
- **@Etch_vps_bot (H1)**: secondary VPS bot/service checks

Use clear per-bot reporting to avoid ambiguity.

---

## 9) Online references reviewed

### Official (trusted)
- https://docs.openclaw.ai/vps
- https://docs.openclaw.ai/install
- https://docs.openclaw.ai/gateway/security
- https://docs.openclaw.ai/help/environment
- https://docs.openclaw.ai/install/hetzner

### Community/third-party (use with judgment)
- Pulumi blog: OpenClaw on AWS/Hetzner + Tailscale
- Security hardening writeups (Substack/independent blogs)

Rule: prefer official docs first; use third-party posts for ideas, not as sole source of truth.

---

## 10) Maintenance rhythm

Weekly:
- `openclaw status`
- `openclaw doctor`
- `openclaw security audit`
- Verify backups restore correctly

After any change:
- Re-run `doctor` + `security audit`
- Confirm channel routing and bot reachability

---

If needed, extend this file with:
- exact per-bot health commands
- VPS bootstrap script
- incident recovery runbook
