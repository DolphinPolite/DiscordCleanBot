
import discord
from discord import Embed
from discord.ui import Button, View
from discord.ext import commands, tasks
from itertools import cycle 
from dotenv import load_dotenv
import os
from function import Cleaner, Starter

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

bot_status = cycle(["1", "2", "3", "4"])

load_dotenv()

SPEELS = []

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

@bot.event
async def on_ready():
    channel = bot.get_channel(1007625208443703366)
    await channel.send("Yor'ue Bluetooth Device Is Connected Successfully!")
    change_status.start()

    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occurred", e)

@bot.tree.command(name="clean", description="You get recommendation about cleaning")
async def pvp(interaction: discord.Interaction):
    await interaction.response.defer()

    await Starter(interaction=interaction)

bot.run(os.getenv("TOKEN"))
