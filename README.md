# 🎮 Steam Discord Watcher Bot

Ein robuster, asynchroner Python-Bot, der erkennt, wenn ein Steam-Nutzer ein Spiel startet, und das in einem Discord-Channel postet.

---

## 📦 Projektstruktur

```bash
steam-discord-watcher/
├── bot.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Features

- **Asynchrone** Steam API-Abfragen mit `aiohttp`
- **Automatisches Laden** von Umgebungsvariablen via `python-dotenv`
- **Graceful Error-Handling** & **Logging** via `logging`
- **Env-Validation**: Verhindert fehlende Konfiguration
- **Docker- & Docker Compose-ready**

---

## 🛠 Voraussetzungen

- Docker & Docker Compose installiert
- Ein Steam Web API Key (https://steamcommunity.com/dev/apikey)
- Steam64-ID des zu überwachenden Nutzers
- Discord Bot Token mit Schreibrechten im Channel

---

## 🔧 Installation

1. Repository klonen:

   ```bash
   git clone https://github.com/dein-user/steam-discord-watcher.git
   cd steam-discord-watcher
   ```

2. Beispiel-Env kopieren und anpassen:

   ```bash
   cp .env.example .env
   # .env mit deinen Daten befüllen
   ```

3. Container bauen & starten:

   ```bash
   docker-compose up --build -d
   ```

---

## ⚙️ Konfiguration

Konfiguriere die `.env`-Datei:

| Variable           | Beschreibung                                           |
|--------------------|--------------------------------------------------------|
| `STEAM_API_KEY`    | Dein Steam Web API Key                                 |
| `STEAM_ID`         | Steam64-ID des zu überwachenden Nutzers                |
| `DISCORD_TOKEN`    | Discord Bot Token (mit Schreibrechten im Ziel-Channel) |
| `DISCORD_CHANNEL_ID` | ID des Discord-Channels für Benachrichtigungen        |
| `CHECK_INTERVAL`   | Abfrageintervall in Sekunden (Default: `60`)           |

---

## ▶️ Verwendung
Verwende den Befehl !linksteam, um deinen Discord-Account mit deinem Steam-Account zu verknüpfen.

🔹 Befehl:
diff
Kopieren
Bearbeiten
!linksteam <steam64_id>
🔹 Beispiel:
diff
Kopieren
Bearbeiten
!linksteam 76561198012345678
🔹 Was passiert danach?
Deine Steam64-ID wird lokal gespeichert.

Der Bot prüft regelmäßig, ob du ein Spiel spielst.

Sobald du etwas spielst, wird automatisch eine Nachricht im konfigurierten Discord-Channel gepostet.

💡 Die Steam64-ID ist eine lange Zahl (meist 17-stellig), die mit 765 beginnt. Du findest sie z. B. über https://steamid.io/.




- Sobald der Bot läuft, überprüft er alle `CHECK_INTERVAL` Sekunden den Spielstatus.
- Erkennt er ein neues Spiel, sendet er eine Nachricht:

  ```
  🎮 Dein Freund spielt jetzt <Spielname>!
  ```

---

## 🐞 Troubleshooting

- **Bot startet nicht?**  
  - Prüfe, ob alle Umgebungsvariablen gesetzt sind.
  - In Docker-Logs (`docker-compose logs`) siehst du Fehlermeldungen.

- **Kein Eintrag im Channel?**  
  - Stelle sicher, dass der Bot Schreibrechte hat.
  - Überprüfe die `DISCORD_CHANNEL_ID`.

---

## 📄 Lizenz

MIT
