import os
import json
import asyncio
import discord
import aiohttp
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

LINKED_USERS_FILE = "linked_users.json"

def load_linked_users():
    if not os.path.exists(LINKED_USERS_FILE):
        return {}
    with open(LINKED_USERS_FILE, "r") as f:
        return json.load(f)

def save_linked_users(data):
    with open(LINKED_USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

linked_users = load_linked_users()
last_game = {}  # discord_id: game

@bot.event
async def on_ready():
    print(f"✅ Bot eingeloggt als {bot.user}")
    check_steam_status.start()

@bot.command()
async def linksteam(ctx, steam_id: str):
    if not steam_id.isdigit() or not steam_id.startswith("765"):
        await ctx.send("❌ Ungültige Steam64-ID. Sie sollte mit `765` beginnen und nur aus Zahlen bestehen.")
        return
    discord_id = str(ctx.author.id)
    linked_users[discord_id] = steam_id
    save_linked_users(linked_users)
    await ctx.send(f"✅ Verknüpft mit Steam-ID `{steam_id}`.")

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_steam_status():
    if not linked_users:
        return

    steam_ids = list(linked_users.values())
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={','.join(steam_ids)}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json()
                players = data.get("response", {}).get("players", [])

                for player in players:
                    steam_id = player.get("steamid")
                    game = player.get("gameextrainfo")
                    discord_id = next((k for k, v in linked_users.items() if v == steam_id), None)
                    if not discord_id:
                        continue

                    if game and last_game.get(discord_id) != game:
                        channel = bot.get_channel(DISCORD_CHANNEL_ID)
                        username = player.get("personaname", "Unbekannt")
                        await channel.send(f"🎮 <@{discord_id}> ({username}) spielt jetzt **{game}**!")
                        last_game[discord_id] = game
                    elif not game:
                        last_game[discord_id] = None

        except Exception as e:
            print(f"Fehler bei der Steam-Abfrage: {e}")

bot.run(DISCORD_TOKEN)
