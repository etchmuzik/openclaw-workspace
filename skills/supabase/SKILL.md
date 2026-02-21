---
name: supabase
description: Manage Supabase projects — database (Postgres), auth, storage, edge functions, migrations, local dev, and deployment. Backend-as-a-service for rapid app development. Use when working with Supabase CLI, managing database schemas/migrations, configuring auth providers, storage buckets, writing/deploying edge functions, or linking/deploying to remote Supabase projects.
---

# Supabase

CLI location: `/opt/homebrew/bin/supabase`

## Quick Reference

For common command patterns, see [references/supabase-cli.md](references/supabase-cli.md).

## Key Workflows

### Initialize a Project

```bash
supabase init
```

Creates `supabase/` directory with `config.toml`. Run in project root.

### Link to Remote Project

```bash
supabase link --project-ref <project-id>
```

Get project ID from Supabase dashboard URL or `supabase projects list`.

### Local Development

```bash
supabase start   # Start local stack (Postgres, Auth, Storage, etc.)
supabase status  # Show local service URLs and keys
supabase stop    # Stop local stack
```

Requires Docker. Local dashboard at `http://localhost:54323`.

### Database Migrations

```bash
supabase migration new <name>           # Create blank migration file
supabase db diff --use-migra -f <name>  # Auto-generate migration from local changes
supabase db reset                        # Reset local DB and replay migrations
supabase db push                         # Push migrations to remote
```

Migration files live in `supabase/migrations/`. Write raw SQL.

### Manage Tables (via SQL)

Use migrations or direct SQL. Example migration:

```sql
CREATE TABLE public.todos (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id uuid REFERENCES auth.users(id),
  task text NOT NULL,
  done boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE public.todos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users manage own todos" ON public.todos
  USING (auth.uid() = user_id);
```

### Auth Setup

Auth runs automatically with local dev. Configure providers in `supabase/config.toml`:

```toml
[auth.external.google]
enabled = true
client_id = "env(GOOGLE_CLIENT_ID)"
secret = "env(GOOGLE_CLIENT_SECRET)"
```

### Storage Buckets

```sql
-- In a migration:
INSERT INTO storage.buckets (id, name, public) VALUES ('avatars', 'avatars', true);

CREATE POLICY "Public read" ON storage.objects FOR SELECT USING (bucket_id = 'avatars');
CREATE POLICY "Auth upload" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'avatars' AND auth.role() = 'authenticated');
```

### Edge Functions

```bash
supabase functions new <name>     # Create function scaffold
supabase functions serve           # Serve locally (hot reload)
supabase functions deploy <name>   # Deploy to remote
supabase functions deploy --no-verify-jwt <name>  # Deploy without JWT verification
```

Functions use Deno runtime. Located in `supabase/functions/<name>/index.ts`.

### Deploy to Remote

```bash
supabase db push           # Push migrations
supabase functions deploy  # Deploy all edge functions
```

### Seed Data

Place seed SQL in `supabase/seed.sql`. Runs after migrations on `supabase db reset`.

## Tips

- Always enable RLS on public tables
- Use `supabase gen types typescript --local` to generate TypeScript types from schema
- Use `supabase inspect db` subcommands for database health checks
- Set secrets for edge functions: `supabase secrets set KEY=value`
