# Google Tasks MCP Server

**Package:** `@alvincrave/gtasks-mcp`

## Setup

1. Enable **Google Tasks API** in GCP Console (project: `claude-automation-490723`)
2. Reuse the existing Desktop OAuth client from `gcp-oauth.keys.json`
3. Obtain a refresh token using the Desktop OAuth flow:
   - Open the auth URL with `scope=https://www.googleapis.com/auth/tasks`, `redirect_uri=http://localhost`, `access_type=offline`, `prompt=consent`
   - Copy the `code` param from the localhost redirect URL
   - Exchange via `POST https://oauth2.googleapis.com/token` with `grant_type=authorization_code`
4. Add `google-tasks` entry to `.mcp.json` with `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`

## Available Tools

- `list-tasklists` — List all task lists
- `list-tasks` — List tasks in a task list
- `get-task` — Get a specific task
- `create-task` — Create a new task
- `update-task` — Update an existing task
- `delete-task` — Delete a task

## Notes

- Refresh token expires in ~7 days (test app). To get a long-lived token, publish the app or add the Google account as a test user in the OAuth consent screen.
- The `.mcp.json` file is gitignored since it contains the refresh token.
