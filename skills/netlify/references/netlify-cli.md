# Netlify CLI Reference

## Command Index

| Command | Description |
|---------|-------------|
| `netlify deploy` | Deploy site |
| `netlify sites:list` | List all sites |
| `netlify sites:create` | Create new site |
| `netlify sites:delete` | Delete a site |
| `netlify link` | Link local dir to site |
| `netlify unlink` | Unlink directory |
| `netlify env:list` | List env vars |
| `netlify env:set` | Set env var |
| `netlify env:get` | Get env var value |
| `netlify env:unset` | Remove env var |
| `netlify env:import` | Import from .env file |
| `netlify status` | Auth & link status |
| `netlify open` | Open site in browser |
| `netlify dev` | Local dev server |
| `netlify functions:list` | List functions |
| `netlify functions:create` | Scaffold a function |
| `netlify functions:invoke` | Invoke function locally |
| `netlify logs:function` | Stream function logs |
| `netlify watch` | Watch active deploy |
| `netlify deploy:list` | List recent deploys |

## Common Patterns

### Deploy flow (no git integration)
```bash
# Build your site
npm run build

# Preview deploy
netlify deploy --dir=dist

# If preview looks good, go to production
netlify deploy --dir=dist --prod
```

### Deploy with message
```bash
netlify deploy --dir=dist --prod --message="Release v1.2.0"
```

### Create site and deploy in one go
```bash
netlify sites:create --name=my-app
netlify link --name=my-app
netlify deploy --dir=./build --prod
```

### Environment variable workflow
```bash
# Set for all contexts
netlify env:set API_KEY sk-xxx

# Import bulk from file
netlify env:import .env
```

### Function development
```bash
# Create from template
netlify functions:create --name=hello

# Test locally
netlify dev
curl http://localhost:8888/.netlify/functions/hello

# View production logs
netlify logs:function hello
```

### CI/CD trigger via build hook
```bash
# Create build hook in Netlify UI (Site settings > Build hooks)
# Then trigger:
curl -X POST -d '{}' https://api.netlify.com/build_hooks/YOUR_HOOK_ID
```

### JSON output for scripting
```bash
netlify sites:list --json
netlify env:list --json
netlify deploy --dir=dist --prod --json
```

## Global Flags

- `--site=SITE_ID` — Target a specific site without linking
- `--json` — Output as JSON (useful for scripting)
- `--debug` — Verbose debug output
- `--auth=TOKEN` — Use specific auth token
