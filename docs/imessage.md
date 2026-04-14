# iMessage Integration

Connect Zorro Agent to Apple iMessage via a local [BlueBubbles](https://bluebubbles.app/) server.

## Prerequisites

> **A Mac computer running macOS is required.** There is no way to bridge iMessage without a Mac — Apple does not offer a public iMessage API. The Mac must remain powered on and connected to the internet for the integration to work.

| Requirement | Details |
|---|---|
| **macOS device** | Mac Mini, MacBook, Mac Studio, or Mac Pro. Must stay on 24/7 if you want always-on messaging. |
| **Apple ID** | Signed in to iMessage on the Mac. |
| **BlueBubbles Server** | Free, open-source app that exposes iMessage over a local REST API. |
| **Network access** | Zorro must be able to reach the Mac's IP on the BlueBubbles port (default: 1234). |

## Setup

### Step 1: Install BlueBubbles Server on your Mac

1. Download BlueBubbles from [bluebubbles.app](https://bluebubbles.app/).
2. Open the app and complete the setup wizard.
3. Sign in with your Apple ID when prompted.
4. In **Settings > API**, note the **Server URL** (e.g., `http://192.168.1.42:1234`) and the **API password**.

### Step 2: Configure Zorro

Add the following to `~/.zorro/.env`:

```bash
# BlueBubbles iMessage (required)
BLUEBUBBLES_SERVER_URL=http://192.168.1.42:1234
BLUEBUBBLES_PASSWORD=your-bluebubbles-password

# Optional: restrict who can message the agent
BLUEBUBBLES_ALLOWED_USERS=+15551234567,+15559876543

# Optional: default chat for cron job delivery
BLUEBUBBLES_HOME_CHANNEL=chat_guid_here
BLUEBUBBLES_HOME_CHANNEL_NAME=Home

# Optional: webhook settings (defaults work for most setups)
BLUEBUBBLES_WEBHOOK_HOST=127.0.0.1
BLUEBUBBLES_WEBHOOK_PORT=8645
```

### Step 3: Start the gateway

```bash
zorro gateway
```

You should see `BlueBubbles: connected` in the startup output.

### Step 4: Send a test message

Send an iMessage to the phone number or email associated with the Mac's Apple ID. Zorro will respond in the same conversation.

## How It Works

```
iPhone/iPad ──iMessage──▶ Mac (BlueBubbles Server) ──REST API──▶ Zorro Agent
                                                    ◀──webhook──
```

- **Inbound**: BlueBubbles forwards incoming iMessages to Zorro via a local webhook.
- **Outbound**: Zorro sends replies through the BlueBubbles REST API, which delivers them as iMessages from the Mac's Apple ID.
- **Media**: Images, voice memos, videos, and documents are supported in both directions.
- **Reactions**: Tapback reactions (love, like, laugh, etc.) are supported if BlueBubbles Private API is enabled.

## Capabilities

| Feature | Supported |
|---|---|
| Text messages | Yes |
| Images | Yes (send and receive) |
| Voice memos | Yes |
| Videos | Yes |
| Documents/files | Yes |
| Tapback reactions | Yes (requires Private API helper) |
| Typing indicators | Yes (requires Private API helper) |
| Read receipts | Yes |
| Group chats | Yes |

## Troubleshooting

### "BlueBubbles: aiohttp/httpx missing"

Install the required dependencies:

```bash
pip install aiohttp httpx
```

### Connection refused

- Verify the Mac is running and BlueBubbles Server is open.
- Check that the `BLUEBUBBLES_SERVER_URL` matches the URL shown in BlueBubbles Settings > API.
- If Zorro runs on a different machine, ensure the Mac's firewall allows incoming connections on port 1234.

### Messages not arriving

- Check that the BlueBubbles webhook is registered: open BlueBubbles > Settings > API > Webhooks. You should see Zorro's webhook URL listed.
- Verify `BLUEBUBBLES_WEBHOOK_HOST` is reachable from the Mac. If Zorro runs on the same Mac, `127.0.0.1` is correct. If on a different machine, use that machine's LAN IP.

### Private API features not working

Tapback reactions and typing indicators require the BlueBubbles Private API helper. Follow the [BlueBubbles Private API guide](https://docs.bluebubbles.app/private-api/) to set it up.

## Security Notes

- BlueBubbles runs locally on your Mac. No data passes through third-party servers.
- The API password protects against unauthorized access to the BlueBubbles REST API.
- Use `BLUEBUBBLES_ALLOWED_USERS` to restrict which phone numbers can interact with the agent.
- Phone numbers are automatically redacted in Zorro's log output.
