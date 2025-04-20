import os
import asyncio
import logging

import aiohttp
import discord
from discord import Intents

# ---- Konfiguration & Logging ----

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger(__name__)

REQUIRED_ENV = [
    "STEAM_API_KEY",
    "STEAM_ID",
    "DISCORD_TOKEN",
    "DISCORD_CHANNEL_ID"
]

for var in REQUIRED_ENV:
    if not os.getenv(var):
        log.critical(f"Umgebungsvariable {var} fehlt!")
        raise SystemExit(1)

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))

intents = Intents.default()
intents.presences = True
intents.members = True
bot = discord.Client(intents=intents)

last_game = None

async def fetch_current_game(session: aiohttp.ClientSession) -> str | None:
    url = (
        "https://api.steampowered.com/ISteamUser/"
        f"GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={STEAM_ID}"
    )
    try:
        async with session.get(url, timeout=10) as resp:
            resp.raise_for_status()
            data = await resp.json()
            player = data["response"]["players"][0]
            return player.get("gameextrainfo")
    except Exception as e:
        log.error(f"Fehler beim Abrufen des Steam-Status: {e}")
        return None

async def steam_watcher():
    global last_game
    await bot.wait_until_ready()
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel is None:
        log.critical(f"Channel mit ID {DISCORD_CHANNEL_ID} nicht gefunden!")
        await bot.close()
        return

    async with aiohttp.ClientSession() as session:
        while not bot.is_closed():
            current_game = await fetch_current_game(session)

            if current_game and current_game != last_game:
                await channel.send(f"🎮 Dein Freund spielt jetzt **{current_game}**!")
                log.info(f"Nachricht gesendet: {current_game}")
                last_game = current_game
            elif current_game is None:
                # Fehlerfall, nichts tun
                pass
            else:
                last_game = None

            await asyncio.sleep(CHECK_INTERVAL)

@bot.event
async def on_ready():
    log.info(f"Eingeloggt als {bot.user} (ID: {bot.user.id})")
    bot.loop.create_task(steam_watcher())

if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        log.critical(f"Bot konnte nicht starten: {e}")
