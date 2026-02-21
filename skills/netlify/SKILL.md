---
name: netlify
description: Deploy sites, manage projects, domains, environment variables, serverless functions, forms, and check deploy status on Netlify. Use when working with Netlify hosting, deploying static/JAMstack sites, managing Netlify site settings, DNS, build hooks, deploy logs, or serverless functions.
---

# Netlify

CLI location: `/Users/etch/.nvm/versions/node/v22.17.0/bin/netlify`

Authenticated as: hesham saied (beyondtech.eg@gmail.com)

## Key Workflows

### Deploy a Site

```bash
# Deploy to draft URL (preview)
netlify deploy --dir=./build

# Deploy to production
netlify deploy --dir=./build --prod

# Deploy with a specific site (no need to link)
netlify deploy --dir=./build --site=SITE_ID --prod
```

### List & Manage Sites

```bash
netlify sites:list
netlify sites:create --name=my-site
netlify sites:delete SITE_ID
```

### Link/Unlink Project

```bash
netlify link --id=SITE_ID
netlify unlink
```

### Environment Variables

```bash
netlify env:list
netlify env:set KEY value
netlify env:get KEY
netlify env:unset KEY
netlify env:import .env
```

### Domains & DNS

```bash
netlify domains:list --site=SITE_ID
# Custom domains are managed in site settings or via API
```

### Deploy Status & Logs

```bash
netlify status
netlify deploy:list --site=SITE_ID
netlify watch          # Watch current deploy
netlify logs:function FUNCTION_NAME
```

### Serverless Functions

```bash
netlify functions:list
netlify functions:create FUNCTION_NAME
netlify functions:invoke FUNCTION_NAME
netlify functions:serve  # Local dev server for functions
```

### Build Hooks

```bash
# Trigger a build via curl with a build hook URL
curl -X POST -d '{}' https://api.netlify.com/build_hooks/HOOK_ID
```

### Local Development

```bash
netlify dev            # Start local dev server with Netlify features
netlify dev --live     # Share live dev server
```

## Reference

For detailed CLI command patterns, see [references/netlify-cli.md](references/netlify-cli.md).
