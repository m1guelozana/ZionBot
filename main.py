import discord
from discord.ext import commands
import json
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"] or os.getenv("token") 
    prefix = data["prefix"] or os.getenv("prefix")  
    owner_id = data["owner_id"] or os.getenv("owner_id")  

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True  

# The bot
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Load cogs
# Load cogs asynchronously
async def load_cogs():
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")  
            print(f"Loaded cog: {filename[:-3]}")  


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print(discord.__version__)
    print(f"My Prefix: {prefix}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"
        )
    )
    
@bot.event
async def on_command(ctx):
    print(f"Command {ctx.command} invoked by {ctx.author}.")
    

async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

import asyncio
asyncio.run(main())