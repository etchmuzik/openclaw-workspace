#!/bin/bash
# Validate OpenClaw config before applying changes

CONFIG_FILE="${1:-$HOME/.openclaw/openclaw.json}"

echo "🔍 Validating config: $CONFIG_FILE"

# Check if file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

# Check if it's valid JSON
if ! python3 -m json.tool "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "❌ Invalid JSON syntax"
    exit 1
fi

echo "✅ Valid JSON syntax"

# Run OpenClaw's validator
if openclaw doctor --config "$CONFIG_FILE" 2>&1 | grep -q "Config invalid"; then
    echo "❌ OpenClaw validation failed"
    openclaw doctor --config "$CONFIG_FILE" 2>&1 | grep -A5 "Problem:"
    exit 1
fi

echo "✅ OpenClaw validation passed"
echo "✅ Config is valid"
exit 0
