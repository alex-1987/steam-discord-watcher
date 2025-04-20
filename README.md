# Steam Discord Dynamic Watcher

Ein Discord-Bot, der automatisch überprüft, welche Discord-Nutzer aktuell ein Steam-Spiel spielen – basierend auf verknüpften Steam-IDs.

## 🔧 Setup

1. **Repo klonen & in das Verzeichnis wechseln**  
   ```bash
   git clone <repo-url>
   cd steam-discord-dynamic-watcher
   ```

2. **`.env` Datei erstellen**  
   Kopiere die `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Trage deine Tokens & Channel-ID ein.

3. **Docker verwenden (empfohlen)**  
   ```bash
   docker build -t steam-discord-bot .
   docker run --env-file .env steam-discord-bot
   ```

   Alternativ lokal:
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```

## 💬 Verwendung

- `!linksteam <steam64_id>` – Verknüpft deinen Discord-Account mit deiner Steam64-ID

Beispiel:
```
!linksteam 76561198012345678
```

Der Bot wird automatisch regelmäßig prüfen, ob du ein Spiel spielst, und es im angegebenen Channel posten.

## ❗ Hinweise

- Die Steam64-ID beginnt **immer mit `765`** und ist eine 17-stellige Zahl.
- Der Bot benötigt mindestens `Send Messages`-Berechtigung im Channel.
- Die Steam API hat Ratenbegrenzungen – also nicht zu oft pollen.

## ✅ .env Beispiel

```env
DISCORD_TOKEN=dein_token
DISCORD_CHANNEL_ID=123456789012345678
STEAM_API_KEY=dein_steam_api_key
CHECK_INTERVAL=60
```
