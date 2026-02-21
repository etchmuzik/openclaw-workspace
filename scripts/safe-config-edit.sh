#!/bin/bash
# Safe config editing wrapper
# Always validates before applying changes

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
TEMP_FILE="/tmp/openclaw-config-edit.json"

# Backup first
bash "$(dirname "$0")/backup-config.sh"

# Copy to temp for editing
cp "$CONFIG_FILE" "$TEMP_FILE"

echo ""
echo "⚠️  Config copied to: $TEMP_FILE"
echo "Edit the temp file, then this script will validate and apply."
echo ""
read -p "Press Enter when ready to validate..."

# Validate
if bash "$(dirname "$0")/validate-config.sh" "$TEMP_FILE"; then
    echo ""
    read -p "✅ Valid! Apply changes? (y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        cp "$TEMP_FILE" "$CONFIG_FILE"
        echo "✅ Config applied"
    else
        echo "❌ Cancelled"
    fi
else
    echo ""
    echo "❌ Validation failed - config NOT applied"
    echo "Temp file preserved at: $TEMP_FILE"
    exit 1
fi
