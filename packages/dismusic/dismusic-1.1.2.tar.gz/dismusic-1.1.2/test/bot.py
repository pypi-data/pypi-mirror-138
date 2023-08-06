import os
from discord.ext import commands

os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'true'

bot = commands.Bot(command_prefix="?")

bot.lavalink_nodes = [
    {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains", "identifier": "Beta"},
    {"host": "lava.link", "port": 80, "password": "dismusic", "identifier": "Gamma"},
    {"host": "lavalink.islantay.tk", "port": 8880, "password": "waifufufufu", "identifier": "WTF"},
    {"host": "node1.lavalink.eu", "port": 2333, "password": "Raccoon", "identifier": "Alpha"},
]

bot.load_extension("dismusic")

@bot.event
async def on_ready():
    print(f"Bot is ready {bot.user.name}")

bot.run("NzI5Njg3Mzg3MTMwNjkxNjY1.XwMkVg.CP00J8ztfYt67mGuWofcrH01s8I")