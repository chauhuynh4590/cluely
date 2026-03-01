# Cluely — Chat Translation Add-on

Cluely is a pluggable chat translation tool that lets you communicate in any language. Type in your native language and Cluely translates your messages to whatever language you need. Currently supports **Slack**, designed to be extensible to any chat platform.

## Features

- **Slash command** — `/translate es Hello world` translates and posts to the channel
- **Auto-translate channel** — `/translate-channel ja` auto-translates all messages in threads
- **Message shortcut** — Right-click any message to translate it (ephemeral, only you see it)
- **Flag emoji reactions** — React with a flag emoji (e.g. :flag-fr:) to translate in a thread
- **Pluggable translation backends** — OpenAI (high quality), Google Translate (free), DeepL
- **Translation caching** — LRU cache to avoid redundant API calls

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A Slack workspace where you can install apps

### Installation

```bash
# Clone the repo
git clone https://github.com/your-org/cluely.git
cd cluely

# Install dependencies
uv sync

# Copy and configure environment
cp .env.example .env
# Edit .env with your Slack tokens and API keys
```

### Slack App Setup

Follow the detailed guide in [scripts/setup_slack_app.md](scripts/setup_slack_app.md) to create and configure your Slack app.

### Running

```bash
uv run cluely
```

## Configuration

All configuration is via environment variables (or a `.env` file):

| Variable | Required | Default | Description |
|---|---|---|---|
| `SLACK_BOT_TOKEN` | Yes | — | Slack bot OAuth token (`xoxb-...`) |
| `SLACK_APP_TOKEN` | Yes | — | Slack app-level token for Socket Mode (`xapp-...`) |
| `SLACK_SIGNING_SECRET` | No | — | Slack signing secret for request verification |
| `TRANSLATION_PROVIDER` | No | `google` | Translation backend: `openai`, `google`, or `deepl` |
| `OPENAI_API_KEY` | If using openai | — | OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | OpenAI model to use |
| `DEEPL_API_KEY` | If using deepl | — | DeepL API key |
| `DATABASE_PATH` | No | `cluely.db` | SQLite database path for channel settings |
| `DEFAULT_TARGET_LANGUAGE` | No | `en` | Fallback target language |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `CACHE_MAX_SIZE` | No | `1000` | Max cached translations |

## Usage

### Slash Commands

```
/translate es Hello, how are you?
/translate ja Good morning everyone
```

### Auto-Translate Channel

```
/translate-channel fr       # Enable: translate all messages to French
/translate-channel off      # Disable auto-translation
```

### Message Shortcut

1. Hover over any message
2. Click the "..." menu or lightning bolt
3. Select "Translate Message"
4. Enter the target language code
5. See the translation (only visible to you)

### Flag Emoji Reactions

React on any message with a country flag emoji:
- :flag-fr: → French
- :flag-es: → Spanish
- :flag-jp: → Japanese
- :flag-de: → German
- ...and many more (see `src/cluely/platform/slack/emoji_map.py`)

## Architecture

```
src/cluely/
├── config.py              # Pydantic Settings
├── main.py                # Entry point
├── translation/           # Pluggable translation providers
│   ├── base.py            # TranslationProvider ABC
│   ├── openai_provider.py # OpenAI/LLM
│   ├── google_provider.py # Google Translate (free)
│   ├── deepl_provider.py  # DeepL
│   ├── cache.py           # LRU cache wrapper
│   └── registry.py        # Provider factory
├── platform/              # Chat platform integrations
│   ├── base.py            # ChatPlatform ABC
│   └── slack/             # Slack implementation
└── storage/               # Persistence
    ├── base.py            # SettingsStore ABC
    └── sqlite_store.py    # SQLite implementation
```

### Adding a New Translation Provider

1. Create `src/cluely/translation/my_provider.py` implementing `TranslationProvider`
2. Add it to `registry.py`
3. Set `TRANSLATION_PROVIDER=my_provider` in `.env`

### Adding a New Chat Platform

1. Create `src/cluely/platform/discord/` (or similar)
2. Implement `ChatPlatform` ABC
3. Wire it up in `main.py`

## Development

```bash
# Install with dev dependencies
uv sync

# Run tests
uv run pytest

# Lint
uv run ruff check src/

# Format
uv run ruff format src/
```

## License

MIT
