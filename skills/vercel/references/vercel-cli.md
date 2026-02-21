# Vercel CLI Reference

## Global Flags

| Flag | Description |
|------|-------------|
| `--yes` / `-y` | Skip confirmation prompts |
| `--token <t>` | Use specific auth token |
| `--scope <team>` | Execute as team |
| `--cwd <dir>` | Set working directory |
| `--debug` | Verbose output |

## Deploy

```bash
vercel [dir]                    # Preview deploy
vercel --prod [dir]             # Production deploy
vercel --prebuilt               # Deploy pre-built output (.vercel/output)
vercel --archive=tgz            # Archive deploy
vercel --env KEY=VAL            # Set build env var
vercel --build-env KEY=VAL      # Set build-only env var
vercel --force                  # Force new deployment (skip cache)
vercel --no-wait                # Don't wait for deployment to complete
```

## Projects

```bash
vercel project ls
vercel project add <name>
vercel project rm <name>
```

## Deployments

```bash
vercel ls [project] [--limit N]
vercel inspect <url>
vercel logs <url> [--follow]
vercel redeploy <url>
vercel remove <deployment> [--safe]   # Remove deployment
```

## Domains

```bash
vercel domains ls
vercel domains add <domain> [project]
vercel domains rm <domain>
vercel domains inspect <domain>
vercel domains move <domain> <destination>
vercel domains transfer-in <domain>
```

## DNS

```bash
vercel dns ls <domain>
vercel dns add <domain> <name> <type> <value>
vercel dns rm <id>
```

## Environment Variables

```bash
vercel env ls [environment]
vercel env add <key> [environment] [gitbranch]
vercel env rm <key> [environment] [gitbranch]
vercel env pull [file]
```

Environments: `production`, `preview`, `development`

## Certs & Secrets

```bash
vercel certs ls
vercel certs issue <domain>
```

## Promote & Rollback

```bash
vercel promote <deployment-url>       # Promote to production
vercel rollback [project] [--timeout] # Rollback production
```

## Aliases

```bash
vercel alias ls
vercel alias set <deployment> <alias>
vercel alias rm <alias>
```

## Teams

```bash
vercel teams ls
vercel teams switch [slug]
```

## Other

```bash
vercel dev [--listen port]      # Local dev server
vercel link [--yes]             # Link to project
vercel pull [--environment env] # Pull settings
vercel build                    # Build locally
vercel whoami                   # Current user
vercel login                    # Authenticate
vercel logout                   # Deauthenticate
vercel bisect                   # Bisect deployments to find regression
```
