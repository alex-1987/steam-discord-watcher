# Discord Steam Notifier Bot

Ein einfacher Discord-Bot, der den aktuellen Steam-Spielstatus von verknüpften Nutzern verfolgt und in einem Channel postet, wenn sie ein Spiel starten.

## Features

- Nutzer können ihre Steam-ID mit Discord verknüpfen
- Überwacht regelmäßig den Spielstatus
- Ankündigungen bei Spielstart
- Docker-fähig für einfachen Betrieb

## Installation

### Lokal

1. Python 3.10+ installieren
2. `.env` erstellen basierend auf `.env.example`
3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```
4. Bot starten:
```bash
python main.py
```

### Mit Docker

```bash
docker-compose up --build
```

## Beispiel `.env`

```dotenv
DISCORD_TOKEN=dein_token
STEAM_API_KEY=dein_steam_api_key
CHECK_INTERVAL=60
```

## Kommandos

- `!linksteam <steam64id>` – Verknüpft deine Steam-ID
- `!unlinksteam` – Hebt die Verknüpfung auf

