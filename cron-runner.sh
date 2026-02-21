#!/bin/bash
# OpenClaw Cron Jobs Wrapper
# These run via system cron instead of gateway cron

export OPENCLAW_GATEWAY_TOKEN="AsRxWQ0uSKccRRmWeFpXburOeY6NNkCF"
export HOME="/data/.openclaw"

case "$1" in
  morning)
    # Morning Briefing - 10:30 AM
    curl -s -X POST http://127.0.0.1:18789/api/hooks \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
      -d '{
        "agent": "Malawany",
        "message": "Morning briefing: Check Dubai weather, today's calendar from hesham@beyondmngmt.ae, and unread emails. Send summary to Telegram."
      }' || echo "Failed to send morning briefing"
    ;;
  github)
    # GitHub Check - 12:00 PM weekdays
    curl -s -X POST http://127.0.0.1:18789/api/hooks \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
      -d '{
        "agent": "Malawany",
        "message": "Check GitHub for etchmuzik: list open PRs and issues that need attention. Send summary to Telegram."
      }' || echo "Failed to send GitHub check"
    ;;
  evening)
    # Evening Recap - 9:00 PM
    curl -s -X POST http://127.0.0.1:18789/api/hooks \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
      -d '{
        "agent": "Malawany",
        "message": "Evening recap: Check tomorrow's calendar and any unread emails. Send summary to Telegram."
      }' || echo "Failed to send evening recap"
    ;;
  health)
    # Weekly Health Check - Sunday 12:00 PM
    curl -s -X POST http://127.0.0.1:18789/api/hooks \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
      -d '{
        "agent": "Malawany",
        "message": "Weekly health check: Run system security audit, check for updates, review disk usage. Send report to Telegram."
      }' || echo "Failed to send health check"
    ;;
  *)
    echo "Usage: $0 {morning|github|evening|health}"
    exit 1
    ;;
esac
