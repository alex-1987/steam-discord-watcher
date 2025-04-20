
# Steam Discord Bot

Ein selbstgehosteter Discord-Bot, der regelmäßig überprüft, ob verknüpfte Steam-Nutzer ein Spiel spielen und das dann im jeweiligen Kanal meldet.

## Features

- Jeder Nutzer kann sich selbst mit einer Steam-ID verknüpfen (`!linksteam`)
- Kanalabhängige Benachrichtigungen
- Docker- und Compose-fähig
- Fehlerbehandlung & Logging
- Speicherung der Nutzer in `linked_users.json`

## Setup

1. Erstelle eine `.env` Datei basierend auf `.env.example`
2. Trage deinen Bot-Token und deinen Steam API Key ein
3. Starte den Bot mit Docker Compose

```bash
docker compose up --build
```

## Befehle

- `!linksteam <Steam64-ID>` – Verknüpft deinen Discord-Account mit einer Steam-ID
- `!unlinksteam` – Entfernt die Verknüpfung

## Steam64-ID finden

- Gehe zu [steamid.io](https://steamid.io/)
- Gib dein Steam-Profil ein
- Kopiere die Steam64-ID (beginnt mit 765...)

## Beispiel `.env`

```env
DISCORD_TOKEN=dein_token
STEAM_API_KEY=dein_api_key
CHECK_INTERVAL=60
```

## Beispielausgabe im Chat

```
🎮 @Benutzer (SteamName) spielt jetzt Elden Ring!
```
