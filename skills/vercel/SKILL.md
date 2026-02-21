---
name: vercel
description: Deploy apps, manage projects, domains, environment variables, serverless functions, and check deployments on Vercel. Use when working with Vercel platform tasks including deploying sites, managing production/preview/dev environments, configuring domains, setting env vars, viewing deployment logs, promoting or rolling back deployments.
---

# Vercel

CLI: `vercel` (v44.6.3) — authenticated as `beyondtecheg-4432`.

## Key Workflows

### Deploy

```bash
vercel                          # Preview deployment (current dir)
vercel --prod                   # Production deployment
vercel --yes                    # Skip confirmation prompts
vercel deploy --archive=tgz     # Deploy as archive (faster for large projects)
```

### Projects

```bash
vercel project ls
vercel project add <name>
vercel project rm <name>
vercel inspect <deployment-url>  # Deployment details
```

### Environment Variables

```bash
vercel env ls [environment]              # List (production/preview/development)
vercel env add <key> [environment]       # Add (reads value from stdin)
vercel env rm <key> [environment]        # Remove
vercel env pull .env.local               # Pull env vars to local file
```

To set a value non-interactively:
```bash
echo "value" | vercel env add SECRET_KEY production
```

### Domains

```bash
vercel domains ls
vercel domains add <domain> [project]
vercel domains rm <domain>
vercel domains inspect <domain>
```

### Deployment Status & Logs

```bash
vercel ls                        # List recent deployments
vercel ls <project>              # List deployments for project
vercel logs <deployment-url>     # View build/runtime logs
vercel inspect <deployment-url>  # Full deployment details
```

### Promote & Rollback

```bash
vercel promote <deployment-url>  # Promote a deployment to production
vercel rollback [project]        # Rollback to previous production deployment
```

### Dev & Link

```bash
vercel dev                       # Local dev server with Vercel features
vercel link                      # Link current dir to a Vercel project
vercel pull                      # Pull project settings & env vars
```

## Gotchas

- `vercel` with no args deploys to **preview**, not production. Use `--prod` for production.
- Env vars are scoped to environments (production/preview/development). Specify which.
- `vercel env add` reads value from **stdin** — pipe it or it'll hang waiting for input.
- Use `--yes` / `-y` to skip interactive prompts in automation.
- `vercel link` must be run before `vercel dev` or `vercel env pull` in a new directory.
- For detailed CLI reference, see [references/vercel-cli.md](references/vercel-cli.md).
