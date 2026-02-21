#!/bin/bash
# Restore OpenClaw config from backup

BACKUP_DIR="$HOME/.openclaw/backups"
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
AUTH_FILE="$HOME/.openclaw/agents/main/agent/auth-profiles.json"

# List available backups
echo "📦 Available config backups:"
echo ""
ls -lht "$BACKUP_DIR"/openclaw_*.json 2>/dev/null | head -10 | awk '{print $9}' | nl

echo ""
read -p "Enter backup number to restore (or 'latest' for most recent): " choice

if [ "$choice" = "latest" ]; then
    backup=$(ls -t "$BACKUP_DIR"/openclaw_*.json 2>/dev/null | head -1)
else
    backup=$(ls -t "$BACKUP_DIR"/openclaw_*.json 2>/dev/null | sed -n "${choice}p")
fi

if [ -z "$backup" ]; then
    echo "❌ Invalid selection"
    exit 1
fi

echo "Restoring: $(basename $backup)"

# Backup current before restoring
cp "$CONFIG_FILE" "$CONFIG_FILE.before-restore"

# Restore
cp "$backup" "$CONFIG_FILE"

echo "✅ Config restored"
echo "Previous config saved to: $CONFIG_FILE.before-restore"
echo ""
echo "🔍 Run 'openclaw doctor' to verify"
