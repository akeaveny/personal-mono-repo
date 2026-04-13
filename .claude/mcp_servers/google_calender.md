# Google Calendar MCP Server

**Package:** `@cocal/google-calendar-mcp`

## Setup

1. Enable **Google Calendar API** in GCP Console (project: `claude-automation-490723`)
2. Reuse the existing Desktop OAuth client from `gcp-oauth.keys.json` (stored in `.claude/mcp_servers/`)
3. Authenticate:
   ```
   GOOGLE_OAUTH_CREDENTIALS=./.claude/mcp_servers/gcp-oauth.keys.json npx -y @cocal/google-calendar-mcp auth
   ```
4. Add `google-calendar` entry to `.mcp.json` with `GOOGLE_OAUTH_CREDENTIALS`

## Available Tools

- `list-calendars` — List all calendars
- `list-events` / `search-events` / `get-event` — Query events
- `create-event` / `create-events` — Create single or multiple events
- `update-event` — Update an existing event
- `delete-event` — Delete an event
- `get-freebusy` — Check free/busy status
- `get-current-time` — Get current time in a timezone
- `respond-to-event` — Accept/decline/tentative an event
- `list-colors` — List available calendar colors
- `manage-accounts` — Manage connected Google accounts

## Notes

- OAuth credentials file lives at `.claude/mcp_servers/gcp-oauth.keys.json`.
- The `.mcp.json` file is gitignored since it contains secrets.
