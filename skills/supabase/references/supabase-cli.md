# Supabase CLI Command Reference

## Project Management

```bash
supabase projects list                    # List all projects
supabase projects create <name> --region <region>  # Create project
supabase init                             # Init local config
supabase link --project-ref <ref>         # Link to remote project
supabase start                            # Start local dev stack
supabase stop                             # Stop local stack
supabase status                           # Show URLs and keys
```

## Database

```bash
supabase migration new <name>             # New blank migration
supabase migration list                   # List migrations and status
supabase db diff --use-migra -f <name>    # Diff local changes into migration
supabase db reset                         # Reset + replay all migrations
supabase db push                          # Apply migrations to remote
supabase db pull                          # Pull remote schema as migration
supabase db dump -f dump.sql              # Dump remote schema
supabase db lint                          # Lint database for issues
supabase inspect db calls                 # Most frequently called queries
supabase inspect db bloat                 # Table bloat
supabase inspect db index-usage           # Index usage stats
```

## Auth

```bash
# Configured via supabase/config.toml [auth] section
# Local auth API at http://localhost:54321/auth/v1
```

## Edge Functions

```bash
supabase functions new <name>             # Scaffold new function
supabase functions serve                  # Local serve with hot reload
supabase functions deploy <name>          # Deploy single function
supabase functions deploy                 # Deploy all functions
supabase functions delete <name>          # Delete deployed function
supabase secrets set KEY=value            # Set function secrets
supabase secrets list                     # List secrets
supabase secrets unset KEY                # Remove secret
```

## Type Generation

```bash
supabase gen types typescript --local     # From local DB
supabase gen types typescript --linked    # From linked remote DB
```

## Storage

```bash
# Managed via SQL migrations (storage.buckets, storage.objects tables)
# Or via dashboard / client libraries
```

## Useful Flags

- `--debug` — Verbose output for troubleshooting
- `--workdir <path>` — Run from a different directory
- `--experimental` — Enable experimental features
