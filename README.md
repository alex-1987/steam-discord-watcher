# Steam Discord Bot

Ein selbstgehosteter Discord-Bot, der anzeigt, wenn Discord-Nutzer, die sich mit ihrem Steam-Konto verknüpft haben, ein Spiel starten.

## Features
- Nutzer können mit `!linksteam <Steam64ID>` ihren Steam-Account verknüpfen.
- Der Bot überwacht den Spielstatus dieser Nutzer und postet automatisch in den Channel, in dem sie den Link gesetzt haben.
- Docker- und Compose-fähig
- Unterstützt mehrere Nutzer gleichzeitig

## Setup

### Voraussetzungen
- Docker & Docker Compose installiert
- Discord Bot erstellt & Token bereit
- Steam API Key

### 1. `.env` Datei erstellen
Kopiere `.env.example` zu `.env` und ergänze deine Daten:

```
DISCORD_TOKEN=dein_discord_token
STEAM_API_KEY=dein_steam_api_key
CHECK_INTERVAL=60
```

### 2. Container starten
```bash
docker-compose up --build -d
```

### 3. Bot verwenden
In einem Discord-Channel:

```bash
!linksteam 7656119XXXXXXXXXX
```

Der Bot wird nun automatisch posten, wenn du ein Spiel startest.

## Verknüpfung aufheben
```bash
!unlinksteam
```

## Sicherheit
- API-Keys werden über Umgebungsvariablen aus `.env` gelesen
- Die Datei `linked_users.json` speichert Verknüpfungen lokal

## Lizenz
MIT