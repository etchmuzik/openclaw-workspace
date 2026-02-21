#!/bin/bash
# Safe OpenClaw config backup script

BACKUP_DIR="$HOME/.openclaw/backups"
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
AUTH_FILE="$HOME/.openclaw/agents/main/agent/auth-profiles.json"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup main config
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$BACKUP_DIR/openclaw_${TIMESTAMP}.json"
    echo "✅ Backed up openclaw.json"
fi

# Backup auth profiles
if [ -f "$AUTH_FILE" ]; then
    cp "$AUTH_FILE" "$BACKUP_DIR/auth-profiles_${TIMESTAMP}.json"
    chmod 600 "$BACKUP_DIR/auth-profiles_${TIMESTAMP}.json"
    echo "✅ Backed up auth-profiles.json"
fi

# Keep only last 10 backups
cd "$BACKUP_DIR"
ls -t openclaw_*.json 2>/dev/null | tail -n +11 | xargs -r rm
ls -t auth-profiles_*.json 2>/dev/null | tail -n +11 | xargs -r rm

echo "✅ Config backed up to: $BACKUP_DIR"
echo "Latest: openclaw_${TIMESTAMP}.json"
