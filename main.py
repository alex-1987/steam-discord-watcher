
import os
import json
import asyncio
import discord
import aiohttp
from discord.ext import commands, tasks
from dotenv import load_dotenv
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Lade Umgebungsvariablen
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

if not DISCORD_TOKEN:
    logging.error("Fehler: DISCORD_TOKEN nicht in .env-Datei gefunden.")
    exit(1)
if not STEAM_API_KEY:
    logging.error("Fehler: STEAM_API_KEY nicht in .env-Datei gefunden.")
    exit(1)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
LINKED_USERS_FILE = "linked_users.json"

def load_linked_users():
    if not os.path.exists(LINKED_USERS_FILE):
        logging.info(f"'{LINKED_USERS_FILE}' nicht gefunden, erstelle neue Datenstruktur.")
        return {}
    try:
        with open(LINKED_USERS_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                logging.error(f"'{LINKED_USERS_FILE}' enthält ungültiges Format (kein Dictionary).")
                return {}
            migrated_data = {}
            needs_migration = False
            for discord_id, value in data.items():
                if isinstance(value, str):
                    migrated_data[discord_id] = {"steam_id": value, "channel_id": None, "last_game": None}
                    needs_migration = True
                elif isinstance(value, dict) and "steam_id" in value:
                    migrated_data[discord_id] = {
                        "steam_id": value.get("steam_id"),
                        "channel_id": value.get("channel_id"),
                        "last_game": value.get("last_game")
                    }
                else:
                    logging.warning(f"Ungültiger Eintrag für Discord-ID {discord_id} in '{LINKED_USERS_FILE}'. Überspringe.")
            if needs_migration:
                logging.info("Datenstruktur in '{LINKED_USERS_FILE}' migriert. Speichere neue Struktur.")
                save_linked_users(migrated_data)
                return migrated_data
            logging.info(f"'{LINKED_USERS_FILE}' erfolgreich geladen.")
            return data
    except json.JSONDecodeError:
        logging.error(f"Fehler beim Dekodieren von JSON aus '{LINKED_USERS_FILE}'. Datei möglicherweise beschädigt.")
        return {}
    except Exception as e:
        logging.error(f"Unerwarteter Fehler beim Laden von '{LINKED_USERS_FILE}': {e}")
        return {}

def save_linked_users(data):
    try:
        with open(LINKED_USERS_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        logging.error(f"Fehler beim Schreiben nach '{LINKED_USERS_FILE}': {e}")
    except Exception as e:
        logging.error(f"Unerwarteter Fehler beim Speichern nach '{LINKED_USERS_FILE}': {e}")

linked_users_data = load_linked_users()

@bot.event
async def on_ready():
    logging.info(f"✅ Bot eingeloggt als {bot.user.name} (ID: {bot.user.id})")
    check_steam_status.start()
    logging.info("Steam-Status-Checker Task gestartet.")

@bot.command(name="linksteam")
async def linksteam(ctx, steam_id: str):
    discord_id = str(ctx.author.id)
    channel_id = ctx.channel.id
    if not steam_id.isdigit() or not steam_id.startswith("765"):
        await ctx.send("❌ Ungültige Steam64-ID.")
        return
    if discord_id in linked_users_data and linked_users_data[discord_id].get("steam_id") == steam_id:
        await ctx.send(f"ℹ️ Bereits verknüpft mit Steam-ID {steam_id}.")
        return
    linked_users_data[discord_id] = {"steam_id": steam_id, "channel_id": channel_id, "last_game": None}
    save_linked_users(linked_users_data)
    await ctx.send(f"✅ Verknüpft mit Steam-ID {steam_id}.")
    logging.info(f"Discord-ID {discord_id} mit Steam-ID {steam_id} verknüpft.")

@bot.command(name="unlinksteam")
async def unlinksteam(ctx):
    discord_id = str(ctx.author.id)
    if discord_id in linked_users_data:
        steam_id = linked_users_data[discord_id].get("steam_id")
        del linked_users_data[discord_id]
        save_linked_users(linked_users_data)
        await ctx.send(f"✅ Verknüpfung mit Steam-ID {steam_id} aufgehoben.")
    else:
        await ctx.send("ℹ️ Keine Verknüpfung vorhanden.")

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_steam_status():
    if not linked_users_data:
        return
    steam_ids = [data.get("steam_id") for data in linked_users_data.values() if data.get("steam_id")]
    if not steam_ids:
        return
    steam_ids_str = ','.join(steam_ids)
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_ids_str}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    logging.error(f"Steam API Fehler: {response.status}")
                    return
                data = await response.json()
                players = data.get("response", {}).get("players", [])
                for player in players:
                    steam_id = player.get("steamid")
                    current_game = player.get("gameextrainfo")
                    discord_id = next((d_id for d_id, u in linked_users_data.items() if u.get("steam_id") == steam_id), None)
                    if not discord_id:
                        continue
                    user_data = linked_users_data[discord_id]
                    last_game = user_data.get("last_game")
                    channel_id = user_data.get("channel_id")
                    if current_game and current_game != last_game:
                        channel = bot.get_channel(channel_id)
                        if channel:
                            username = player.get("personaname", "Unbekannt")
                            try:
                                await channel.send(f"🎮 <@{discord_id}> ({username}) spielt jetzt **{current_game}**!")
                            except Exception as e:
                                logging.warning(f"Fehler beim Senden der Nachricht: {e}")
                        user_data["last_game"] = current_game
                        save_linked_users(linked_users_data)
                    elif not current_game and last_game:
                        user_data["last_game"] = None
                        save_linked_users(linked_users_data)
        except Exception as e:
            logging.error(f"Fehler bei der Steam-Abfrage: {e}")

if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
