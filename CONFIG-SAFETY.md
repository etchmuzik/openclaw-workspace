# CONFIG SAFETY RULES 🛡️

## NEVER do this:
1. ❌ Direct edit `/data/.openclaw/openclaw.json` without backup
2. ❌ Manual JSON edits without validation
3. ❌ Overwrite auth-profiles.json without permission check
4. ❌ Skip validation after config changes
5. ❌ Apply config changes from untrusted sources

## ALWAYS do this:
1. ✅ Backup before ANY config change
2. ✅ Validate after editing
3. ✅ Use OpenClaw CLI commands when possible (`openclaw models`, `openclaw configure`, etc.)
4. ✅ Test in a temp file first
5. ✅ Keep last 10 backups

## Safe config workflow:

### Method 1: Use OpenClaw CLI (SAFEST)
```bash
# Always prefer official commands
openclaw models set <model>
openclaw models aliases add <alias> <model>
openclaw models fallbacks add <model>
openclaw configure --section <section>
```

### Method 2: Manual edit with validation
```bash
# 1. Backup first
bash ~/workspace/scripts/backup-config.sh

# 2. Edit config
nano /data/.openclaw/openclaw.json

# 3. Validate before using
bash ~/workspace/scripts/validate-config.sh

# 4. If invalid, restore
bash ~/workspace/scripts/restore-config.sh
```

### Method 3: Safe edit wrapper
```bash
bash ~/workspace/scripts/safe-config-edit.sh
# Handles backup + validation automatically
```

## Backup locations:
- **Auto backups:** `~/.openclaw/backups/`
- **OpenClaw backups:** `~/.openclaw/openclaw.json.bak` (last change only)
- **Manual backups:** Encouraged before major changes

## Recovery:
```bash
# List backups
ls -lht ~/.openclaw/backups/

# Restore latest
bash ~/workspace/scripts/restore-config.sh
# Choose 'latest' when prompted

# Verify after restore
openclaw doctor
openclaw models status
```

## What I (Malawany) will do:
- **Always backup before config changes**
- **Use CLI commands over manual JSON edits**
- **Validate immediately after changes**
- **Tell you when I'm about to modify config**
- **Never apply invalid configs**
- **Keep you informed of what changed**

## Emergency restore:
```bash
# If OpenClaw won't start due to bad config
cp ~/.openclaw/backups/openclaw_$(ls -t ~/.openclaw/backups/ | head -1) ~/.openclaw/openclaw.json
openclaw gateway restart
```

---
**Rule #1:** When in doubt, backup first. Always.
