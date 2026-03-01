# Slack App Setup Guide

Follow these steps to configure a Slack app for Cluely.

## 1. Create a Slack App

1. Go to https://api.slack.com/apps
2. Click **Create New App** > **From scratch**
3. Name it `Cluely Translator` and select your workspace
4. Click **Create App**

## 2. Enable Socket Mode

1. Go to **Settings > Socket Mode**
2. Toggle **Enable Socket Mode** to ON
3. Give the token a name (e.g. `cluely-socket`) and click **Generate**
4. Copy the `xapp-...` token — this is your `SLACK_APP_TOKEN`

## 3. Add Slash Commands

Go to **Features > Slash Commands** and create two commands:

### /translate
- **Command**: `/translate`
- **Short Description**: Translate a message to another language
- **Usage Hint**: `<lang> <message>` (e.g. `es Hello world`)

### /translate-channel
- **Command**: `/translate-channel`
- **Short Description**: Enable/disable auto-translation for this channel
- **Usage Hint**: `<lang>` or `off`

## 4. Add Message Shortcut

1. Go to **Features > Interactivity & Shortcuts**
2. Ensure **Interactivity** is toggled ON
3. Under **Shortcuts**, click **Create New Shortcut**
4. Select **On messages**
5. **Name**: `Translate Message`
6. **Short Description**: Translate this message to another language
7. **Callback ID**: `translate_message`
8. Click **Create**

## 5. Subscribe to Bot Events

Go to **Features > Event Subscriptions**:

1. Toggle **Enable Events** to ON
2. Under **Subscribe to bot events**, add:
   - `message.channels` — listen to messages in public channels
   - `message.groups` — listen to messages in private channels
   - `reaction_added` — listen for emoji reactions (flag-based translation)

## 6. Set OAuth Scopes

Go to **Features > OAuth & Permissions** and add these **Bot Token Scopes**:

- `chat:write` — post messages and translations
- `commands` — handle slash commands
- `channels:history` — read messages for auto-translate and reactions
- `groups:history` — read messages in private channels
- `reactions:read` — read emoji reactions for flag-based translation

## 7. Install App to Workspace

1. Go to **Settings > Install App**
2. Click **Install to Workspace** and authorize
3. Copy the **Bot User OAuth Token** (`xoxb-...`) — this is your `SLACK_BOT_TOKEN`
4. Go to **Settings > Basic Information** and copy the **Signing Secret** — this is your `SLACK_SIGNING_SECRET`

## 8. Configure Environment

Copy `.env.example` to `.env` and fill in the values:

```bash
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-socket-token
```

## 9. Invite the Bot

In Slack, invite the bot to channels where you want translation:

```
/invite @Cluely Translator
```

## 10. Run the App

```bash
uv run cluely
```

You should see `Cluely is starting...` in the logs. Try `/translate es Hello!` in a channel.
