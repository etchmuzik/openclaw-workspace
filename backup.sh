#!/bin/bash
# Cloud Backup Script — Run daily or on demand
# Pushes all 3 workspaces to GitHub

set -e

echo "🔄 Backing up workspaces..."

cd /data/.openclaw/workspace
git pull origin main --rebase || true
git add -A
git commit -m "Auto-backup: $(date -u +%Y-%m-%d-%H:%M) UTC" || true
git push origin main || echo "Main workspace push failed (remote may not be set up)"

cd /data/.openclaw/workspace-coder
git pull origin main --rebase || true
git add -A
git commit -m "Auto-backup: $(date -u +%Y-%m-%d-%H:%M) UTC" || true
git push origin main || echo "Coder workspace push failed (remote may not be set up)"

cd /data/.openclaw/workspace-researcher
git pull origin main --rebase || true
git add -A
git commit -m "Auto-backup: $(date -u +%Y-%m-%d-%H:%M) UTC" || true
git push origin main || echo "Researcher workspace push failed (remote may not be set up)"

# Backup config
cp /data/.openclaw/openclaw.json /data/.openclaw/openclaw.json.backup

echo "✅ Backup complete"
