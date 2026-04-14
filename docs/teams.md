# Microsoft Teams Integration

Connect Zorro Agent to Microsoft Teams as a bot using the Azure Bot Framework.

## Prerequisites

| Requirement | Details |
|---|---|
| **Microsoft 365 account** | With permission to install custom bots (admin approval may be required). |
| **Azure account** | Free tier is sufficient for bot registration. |
| **Public HTTPS endpoint** | The bot webhook must be reachable from Microsoft's servers. Use a reverse proxy (nginx, Caddy) or a tunnel (ngrok, Cloudflare Tunnel) during development. |

## Setup

### Step 1: Register an Azure Bot

1. Go to [Azure Portal](https://portal.azure.com/) > Create a resource > search "Azure Bot".
2. Create a new Azure Bot with:
   - **Bot handle**: Choose a unique name (e.g., `zorro-agent`).
   - **Type of app**: Multi Tenant.
   - **Creation type**: Create new Microsoft App ID.
3. After creation, go to **Configuration**:
   - Note the **Microsoft App ID**.
   - Click **Manage Password** > **New client secret** > copy the **Value** (this is your App Password).
   - Set **Messaging endpoint** to `https://your-domain.com/api/messages`.

### Step 2: Enable the Teams channel

1. In the Azure Bot resource, go to **Channels** > **Microsoft Teams**.
2. Accept the Terms of Service.
3. Click **Apply** to enable the Teams channel.

### Step 3: Configure Zorro

Add the following to `~/.zorro/.env`:

```bash
# Microsoft Teams (required)
TEAMS_APP_ID=your-microsoft-app-id
TEAMS_APP_PASSWORD=your-microsoft-app-password

# Optional: webhook server settings
TEAMS_WEBHOOK_HOST=0.0.0.0
TEAMS_WEBHOOK_PORT=3978

# Optional: restrict access
TEAMS_ALLOWED_USERS=user1@company.com,user2@company.com
```

### Step 4: Expose the webhook

Microsoft Teams requires a **public HTTPS** endpoint. During development, use a tunnel:

```bash
# Using ngrok
ngrok http 3978

# Using Cloudflare Tunnel
cloudflared tunnel --url http://localhost:3978
```

Copy the HTTPS URL and update the **Messaging endpoint** in Azure Bot Configuration to:

```
https://<your-tunnel-url>/api/messages
```

For production, configure a reverse proxy with a valid TLS certificate.

### Step 5: Install the bot in Teams

1. In the Azure Bot resource, go to **Channels** > **Microsoft Teams** > **Open in Teams**.
2. Or search for the bot by name in the Teams app.
3. Start a conversation — Zorro will respond.

### Step 6: Start the gateway

```bash
pip install "zorro-agent[teams]"
zorro gateway
```

You should see `Teams: connected` in the startup output.

## How It Works

```
Teams User ──message──▶ Microsoft Bot Service ──HTTPS POST──▶ Zorro Agent (port 3978)
                                               ◀──REST API──
```

- **Inbound**: Microsoft Bot Service forwards messages to Zorro's webhook endpoint.
- **Outbound**: Zorro replies via the Bot Framework REST API using stored conversation references.
- **Formatting**: Teams renders Markdown (bold, italic, code blocks, lists, links).

## Capabilities

| Feature | Supported |
|---|---|
| Text messages (Markdown) | Yes |
| Images | Yes (as hero card attachments) |
| Files/documents | Yes (as attachments) |
| Typing indicators | Yes |
| 1:1 conversations | Yes |
| Group/channel conversations | Yes (mention-gated) |
| Adaptive Cards | Planned |
| Voice/video calls | No |

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `TEAMS_APP_ID` | Yes | — | Microsoft App ID from Azure Bot registration |
| `TEAMS_APP_PASSWORD` | Yes | — | Client secret from Azure Bot registration |
| `TEAMS_WEBHOOK_HOST` | No | `0.0.0.0` | Host to bind the webhook server |
| `TEAMS_WEBHOOK_PORT` | No | `3978` | Port for the webhook server |
| `TEAMS_ALLOWED_USERS` | No | — | Comma-separated list of allowed user emails |
| `TEAMS_ALLOW_ALL_USERS` | No | `false` | Set to `true` to allow any user |
| `TEAMS_HOME_CHANNEL` | No | — | Default conversation ID for cron delivery |

## Troubleshooting

### "Teams: botbuilder-core not installed"

Install the Teams dependencies:

```bash
pip install "zorro-agent[teams]"
# or manually:
pip install botbuilder-core botbuilder-integration-aiohttp
```

### Bot not responding in Teams

1. Check that the messaging endpoint in Azure Bot Configuration matches your server URL exactly (including `/api/messages`).
2. Verify the endpoint is reachable from the public internet (test with `curl https://your-url/api/messages`).
3. Check Zorro gateway logs for authentication errors — double-check `TEAMS_APP_ID` and `TEAMS_APP_PASSWORD`.

### "Unauthorized" errors

- The App Password (client secret) may have expired. Create a new one in Azure Portal > App Registrations > Certificates & Secrets.
- Ensure the App ID matches the one registered in the Azure Bot resource.

### Messages delayed or lost

- Microsoft Bot Service has occasional delivery delays (1-5 seconds is normal).
- If messages are consistently lost, check the Azure Bot's **Health** page for service incidents.

## Security Notes

- All communication between Microsoft and your server is over HTTPS with token-based authentication.
- The Bot Framework validates the JWT token on every inbound request — Zorro verifies these tokens automatically.
- Use `TEAMS_ALLOWED_USERS` to restrict access to specific Microsoft 365 accounts.
- For enterprise deployments, consider using Azure Private Link to keep traffic within your VPN.
