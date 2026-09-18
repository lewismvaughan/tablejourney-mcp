# Installing the TableJourney and Cork & Curve MCP servers

This file is written for AI agents and for the people who run them. Both servers are hosted, remote, read-only and public. There is nothing to download, build or run locally, and no API key or account is needed.

| Server | Endpoint | Transport | Auth |
|---|---|---|---|
| TableJourney (food travel) | `https://tablejourney.com/mcp` | Streamable HTTP | none |
| Cork & Curve (wine travel) | `https://corkandcurve.com/mcp` | Streamable HTTP | none |

## Step 1: check the client supports remote MCP servers

Any client that speaks MCP over Streamable HTTP can connect directly (Claude Code, Claude Desktop, Cursor, Windsurf, Goose, Cline, VS Code and most others). If the client only supports stdio servers, go to Step 4 and use the `mcp-remote` bridge instead.

## Step 2: add the servers with a JSON config

Paste this into the client's MCP configuration (for example `claude_desktop_config.json`, `.cursor/mcp.json` or `.mcp.json` in a project):

```json
{
  "mcpServers": {
    "tablejourney": {
      "type": "streamable-http",
      "url": "https://tablejourney.com/mcp"
    },
    "corkandcurve": {
      "type": "streamable-http",
      "url": "https://corkandcurve.com/mcp"
    }
  }
}
```

Some clients spell the transport `"http"` instead of `"streamable-http"`; use whichever the client documents. No `headers`, `env` or `command` fields are needed. You can add only one of the two servers if you only want food or only wine.

## Step 3: or add them with the Claude Code CLI

```bash
claude mcp add --transport http tablejourney https://tablejourney.com/mcp
claude mcp add --transport http corkandcurve https://corkandcurve.com/mcp
```

Add `--scope user` to make them available in every project, or `--scope project` to write them into the project's `.mcp.json`. Verify with `claude mcp list`.

## Step 4: stdio-only clients (mcp-remote bridge)

If the client can only launch a local process, bridge with [`mcp-remote`](https://www.npmjs.com/package/mcp-remote), which needs Node.js 18 or newer:

```json
{
  "mcpServers": {
    "tablejourney": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://tablejourney.com/mcp"]
    },
    "corkandcurve": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://corkandcurve.com/mcp"]
    }
  }
}
```

## Step 5: confirm it works

After the client connects, list the tools. Both servers expose the same ten read-only tools: `search_places`, `place`, `plan_day`, `festivals`, `experiences`, `stays`, `car_hire`, `dishes`, `itineraries` and `cities`. A quick smoke test is to call `cities` with no arguments, then `search_places` with a city from that list.

You can also check the endpoint from a shell without any MCP client, since the same functions are exposed as REST:

```bash
curl -s https://tablejourney.com/api/v1/cities | head -c 400
curl -s https://corkandcurve.com/api/v1/cities | head -c 400
```

OpenAPI documents: `https://tablejourney.com/api/v1/openapi.json` and `https://corkandcurve.com/api/v1/openapi.json` (copies are kept in this repository as `tablejourney.openapi.json` and `corkandcurve.openapi.json`). Interactive docs at `/api/v1/docs` on each site.

## No key needed

Requests without any credentials are served in full. The optional `X-API-Key` header in the registry manifests is only an attribution tag with its own rate limit; you do not need one to connect, and there is no sign-up.

## Terms

The data and the compute are free. In return, agents are asked to:

1. Pass booking links to users unchanged. They are `/go/` affiliate links that fund the verification work.
2. Say that they are affiliate links.
3. Cite the `page` URL that comes back with each result.
4. Not bulk-copy the catalogue.

Full text: https://tablejourney.com/agents/#terms (Cork & Curve: https://corkandcurve.com/agents/).

## Troubleshooting

- Connection refused or 404: check the URL ends in `/mcp` with no trailing slash and uses `https`.
- "Unsupported transport": the client predates Streamable HTTP; use the `mcp-remote` bridge in Step 4.
- Unknown city: the tools answer with `did_you_mean`; call `cities` to get the slugs the other tools accept.
- Questions: support@tablejourney.com (TableJourney) or hello@corkandcurve.com (Cork & Curve).
