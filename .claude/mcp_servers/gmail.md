# Gmail MCP Server

**Package:** `@shinzolabs/gmail-mcp`

## Setup

1. Enable **Gmail API** in GCP Console (project: `claude-automation-490723`)
2. Reuse the existing Desktop OAuth client from `gcp-oauth.keys.json` (stored in `.claude/mcp_servers/`)
3. Auth is handled via the OAuth credentials file; the server runs on port 3001
4. Add `gmail` entry to `.mcp.json` with `GOOGLE_OAUTH_CREDENTIALS` and `PORT`

## Available Tools

- `create_draft` / `get_draft` / `list_drafts` / `send_draft` / `delete_draft` — Draft management
- `send_message` / `get_message` / `list_messages` / `modify_message` / `trash_message` / `untrash_message` / `delete_message` / `batch_delete_messages` / `batch_modify_messages` — Message operations
- `list_threads` / `get_thread` / `modify_thread` / `trash_thread` / `untrash_thread` / `delete_thread` — Thread operations
- `list_labels` / `create_label` / `get_label` / `update_label` / `patch_label` / `delete_label` — Label management
- `get_profile` — Account profile info
- `get_attachment` — Download attachments
- `list_filters` / `create_filter` / `get_filter` / `delete_filter` — Email filters
- `list_forwarding_addresses` / `create_forwarding_address` / `get_forwarding_address` / `delete_forwarding_address` — Forwarding
- `get_auto_forwarding` / `update_auto_forwarding` — Auto-forwarding settings
- `get_vacation` / `update_vacation` — Vacation responder
- `watch_mailbox` / `stop_mail_watch` — Push notifications

## Notes

- The `.mcp.json` file is gitignored since it contains secrets.
- OAuth credentials file lives at `.claude/mcp_servers/gcp-oauth.keys.json`.
