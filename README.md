# 🎮 Steam Discord Watcher Bot

Ein robuster, asynchroner Python-Bot, der erkennt, wenn ein Steam-Nutzer ein Spiel startet, und das in einem Discord-Channel postet.

## 🚀 Features

- **Asynchrone** Steam API-Abfragen mit `aiohttp`
- **Graceful Error-Handling** & **Logging** via `logging`
- **Umgebungsvariable-Validierung** beim Start
- Docker- und Docker-Compose–ready

## 🛠 Installation

```bash
git clone https://github.com/dein-user/steam-discord-watcher.git
cd steam-discord-watcher
cp .env.example .env
# .env mit deinen Daten befüllen
docker-compose up --build -d
```

## 🔧 Konfiguration

Bearbeite die `.env`:

| Variable           | Beschreibung                          |
|--------------------|----------------------------------------|
| STEAM_API_KEY      | Dein Steam API Key                     |
| STEAM_ID           | Steam64-ID des Spielers                |
| DISCORD_TOKEN      | Dein Discord Bot Token                 |
| DISCORD_CHANNEL_ID | ID des Discord-Channels für Benachr.  |
| CHECK_INTERVAL     | Intervall in Sekunden (Default: 60s)  |

## 📄 Lizenz

MIT
