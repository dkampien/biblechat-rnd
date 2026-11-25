---
created: 2026-07-20
updated: 2026-07-20
---

# Team MCP setup guide: BibleChat, Meta Ads, AdLoops

How to connect our MCP servers to Claude Code (CLI) and Claude Desktop. Works with any Claude account: each server authenticates separately through its own browser OAuth login, so your personal Claude subscription is fine.

## The servers

**BibleChat** (sign in with your `@thebiblechat.com` email):

| Name | URL |
|---|---|
| biblechat-core | `https://mcp.thebiblechat.com/mcp` |
| biblechat-dev | `https://builder.thebiblechat.com/mcp/dev/mcp` |
| biblechat-support | `https://builder.thebiblechat.com/mcp/support/mcp` |
| biblechat-management | `https://builder.thebiblechat.com/mcp/management/mcp` |
| biblechat-builder | `https://builder.thebiblechat.com/mcp/builder/mcp` |
| biblechat-marketing | `https://builder.thebiblechat.com/mcp/marketing/mcp` |
| biblechat-analytics | `https://builder.thebiblechat.com/mcp/analytics/mcp` |

**Third-party** (each has its own login):

| Name         | URL                            | Sign in with                                                                                                                             |
| ------------ | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| facebook-ads | `https://mcp.facebook.com/ads` | Your Facebook account. It must have access to the BibleChat ad account in Meta Business Manager, ask Stefan if you don't have access yet |
| adloops      | `https://adloops.ai/mcp/mcp`   | Your AdLoops account                                                                                                                     |

You do not need all of them. Add only the ones relevant to your role; each one you add takes up context and shows up as tools in every conversation.

## Claude Code (CLI)

Run one command per server you want. The `-s user` flag makes it available in every project on your machine:

```bash
claude mcp add --transport http biblechat-core https://mcp.thebiblechat.com/mcp -s user
claude mcp add --transport http biblechat-dev https://builder.thebiblechat.com/mcp/dev/mcp -s user
claude mcp add --transport http biblechat-support https://builder.thebiblechat.com/mcp/support/mcp -s user
claude mcp add --transport http biblechat-management https://builder.thebiblechat.com/mcp/management/mcp -s user
claude mcp add --transport http biblechat-builder https://builder.thebiblechat.com/mcp/builder/mcp -s user
claude mcp add --transport http biblechat-marketing https://builder.thebiblechat.com/mcp/marketing/mcp -s user
claude mcp add --transport http biblechat-analytics https://builder.thebiblechat.com/mcp/analytics/mcp -s user
claude mcp add --transport http facebook-ads https://mcp.facebook.com/ads -s user
claude mcp add --transport http adloops https://adloops.ai/mcp/mcp -s user
```

Then authenticate:

1. Start (or restart) a Claude Code session.
2. Type `/mcp`. Each new server shows as needing authentication.
3. Select a server and choose **Authenticate**. Your browser opens the OAuth login.
4. Sign in with the account listed for that server in the table above.
5. Back in the session, the server shows as connected and its tools are available under the `mcp__<server-name>__` prefix.

The token is stored in the macOS keychain and reused across sessions, so this is a one-time step per server (until the token expires).

To remove a server later:

```bash
claude mcp remove biblechat-dev -s user
```

## Claude Desktop (app)

Two paths depending on your plan. Try Option A first; fall back to Option B if your plan doesn't offer custom connectors.

### Option A: custom connector (built in, no install)

1. Open Claude Desktop, go to **Settings, then Connectors**.
2. Click **Add custom connector**.
3. Enter a name (e.g. `biblechat-dev`) and paste the server URL.
4. Save, then click **Connect**. The browser OAuth login opens.
5. Sign in with the account listed for that server in the table above.
6. Repeat for each server you need.

### Option B: config file with `mcp-remote` bridge

Use this if the Connectors screen doesn't offer custom connectors on your plan. It runs a small local bridge process per server, which requires Node.js.

Check Node is installed (any recent version):

```bash
node --version
npx --version
```

If missing, install it from [nodejs.org](https://nodejs.org) or via `brew install node`.

Open (or create) the Desktop config file:

```bash
open -a "Visual Studio Code" ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

If the file doesn't exist yet:

```bash
mkdir -p ~/Library/Application\ Support/Claude
printf '{\n  "mcpServers": {}\n}\n' > ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Add an entry per server inside `mcpServers` (this example shows two; copy the pattern for any others you need, using the names and URLs from the table above):

```json
{
  "mcpServers": {
    "biblechat-dev": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://builder.thebiblechat.com/mcp/dev/mcp"]
    },
    "biblechat-core": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.thebiblechat.com/mcp"]
    },
    "facebook-ads": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.facebook.com/ads"]
    },
    "adloops": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://adloops.ai/mcp/mcp"]
    }
  }
}
```

Then:

1. Fully quit Claude Desktop (`Cmd-Q`, not just closing the window).
2. Reopen it and start a new chat.
3. On first use of each server, `mcp-remote` opens the browser OAuth login. Sign in with the account listed for that server in the table above.

## Troubleshooting

- **Server shows but has no tools, or auth fails**: your OAuth login likely used the wrong account. Re-authenticate with the account listed for that server in the table above. For `facebook-ads` specifically, "connected but no useful tools" usually means your Facebook account lacks access to the ad account in Business Manager.
- **Curl test**: a healthy server returns `401` with a `WWW-Authenticate: Bearer` header when hit without credentials. A `404` means the URL is wrong.
  ```bash
  curl -si -X POST https://builder.thebiblechat.com/mcp/dev/mcp \
    -H "Content-Type: application/json" | head -5
  ```
- **Desktop config changes not picked up**: the app only reads the config on launch. Fully quit with `Cmd-Q` and reopen.
- **Claude Code and Claude Desktop configs are separate.** CLI servers live in `~/.claude.json`; Desktop servers live in `~/Library/Application Support/Claude/claude_desktop_config.json` (or the Connectors UI). Adding a server in one does not add it to the other.
