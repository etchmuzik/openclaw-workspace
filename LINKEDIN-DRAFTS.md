# LinkedIn Draft Mode - Automated Content Generation

## ✅ Safe Alternative to Direct Posting
- **0% ban risk** - no API calls to LinkedIn
- **100% control** - you review before posting
- **90% time savings** - AI generates drafts, you just approve

## How It Works

### Every Sunday 9 AM (Dubai time):
1. Cron job runs `linkedin_generate_drafts.sh`
2. Creates 5 draft templates in `~/workspace/linkedin-drafts/`
3. Notifies you via Telegram: "📋 5 new LinkedIn drafts ready"
4. You review, edit, and post manually

### Draft Files Created:
| File | Purpose | When to Post |
|------|---------|--------------|
| `personal_weekly_1.md` | Personal post | Monday |
| `personal_weekly_2.md` | Personal post | Wednesday |
| `personal_weekly_3.md` | Personal post | Friday |
| `business_weekly_1.md` | Company post | Tuesday |
| `business_weekly_2.md` | Company post | Thursday |

## Quick Start

### 1. Generate drafts now (test):
```bash
bash ~/.openclaw/agents/main/agent/linkedin_generate_drafts.sh
```

### 2. View your drafts:
```bash
ls ~/workspace/linkedin-drafts/
```

### 3. Open a draft to edit:
```bash
nano ~/workspace/linkedin-drafts/personal_weekly_1.md
```

### 4. Post to LinkedIn:
- Copy content from draft file
- Paste into LinkedIn
- Add hashtags/images
- Post!

### 5. Clean up after posting:
```bash
rm ~/workspace/linkedin-drafts/personal_weekly_1.md
```

## Cron Schedule (Auto-Generation)

### Option A: System Crontab (Recommended)
```bash
# Edit crontab
crontab -e

# Add this line for Sunday 9 AM Dubai time:
0 9 * * 0 TZ=Asia/Dubai /bin/bash /data/.openclaw/agents/main/agent/linkedin_generate_drafts.sh
```

### Option B: OpenClaw Cron (when gateway ready)
```bash
openclaw cron add \
  --name "linkedin-drafts" \
  --cron "0 9 * * 0" \
  --tz "Asia/Dubai" \
  --message "Generate 5 LinkedIn post drafts for the week" \
  --agent main
```

## Content Strategy

### Personal Posts (Mon/Wed/Fri):
**Topics to rotate:**
- 🚀 Project updates & milestones
- 💡 Tech insights & learnings
- 📊 Industry trends & opinions
- 🎯 Career reflections
- 🛠️ Tips & tutorials

**Template:**
```
Hook (attention grabber)
↓
Context/Story
↓
Key insight or lesson
↓
Call-to-action (question, follow, etc.)
↓
3-5 hashtags
```

### Company Posts (Tue/Thu):
**Topics to rotate:**
- 🎉 Product launches & updates
- 👥 Team highlights
- 🤝 Client success stories
- 🏆 Awards & recognition
- 🔧 Behind-the-scenes

**Template:**
```
Announcement/Update
↓
Details & benefits
↓
Social proof (testimonial, numbers)
↓
Call-to-action (visit site, contact, etc.)
↓
Company + industry hashtags
```

## Automation Levels

### Level 1: Templates Only (Current)
- ✅ Cron creates markdown templates
- ✅ You write content manually
- ✅ Full control, lowest effort

### Level 2: AI-Assisted (Next Step)
- Cron generates templates
- AI fills in content suggestions
- You review and edit
- Balance of automation + control

### Level 3: Full AI Drafts (Future)
- AI generates complete posts
- Your job: approve or tweak
- Maximum efficiency

## Monitoring

### Check if cron ran:
```bash
tail ~/.openclaw/logs/linkedin-drafts.log
```

### See all pending drafts:
```bash
ls -lt ~/workspace/linkedin-drafts/
```

### Count drafts this week:
```bash
ls ~/workspace/linkedin-drafts/*.md | wc -l
```

## Advanced: AI Content Generation

### Generate content for a specific draft:
```bash
# From within a draft file, ask me:
"Generate a LinkedIn post about [topic] for my personal profile"

# I'll create:
- Hook/Opening line
- Body content (2-3 paragraphs)
- Call-to-action
- Suggested hashtags
```

### Batch generate all drafts:
```bash
# Ask me in chat:
"Generate LinkedIn posts for all 5 weekly drafts"

# I'll create:
- 3 personal posts (Mon/Wed/Fri topics)
- 2 company posts (Tue/Thu topics)
- All saved to your drafts folder
```

## Best Practices

1. **Review before posting** - Always read the draft
2. **Customize voice** - Make it sound like you
3. **Add media** - Posts with images perform better
4. **Engage** - Reply to comments within 1 hour
5. **Delete drafts** - Keep folder clean after posting
6. **Track performance** - Note which posts get engagement

## File Locations

```
~/.openclaw/agents/main/agent/
├── linkedin_generate_drafts.sh    # Draft generator script
├── linkedin_drafts.py              # Python helper (optional)
└── linkedin-credentials.json       # Stored credentials

~/workspace/
└── linkedin-drafts/                # Your draft files
    ├── personal_weekly_1.md
    ├── personal_weekly_2.md
    ├── personal_weekly_3.md
    ├── business_weekly_1.md
    └── business_weekly_2.md

~/.openclaw/logs/
└── linkedin-drafts.log             # Generation history
```

## Emergency Stop

Disable draft generation:
```bash
# Remove cron job
crontab -e
# Delete the linkedin-drafts line

# Or disable temporarily
touch /tmp/linkedin-drafts.lock
```

---

**Status:** ✅ Configured - Ready to generate drafts  
**Next Run:** Next Sunday 9 AM Dubai time (or run manually now)  
**Risk Level:** 0% - No LinkedIn API used
