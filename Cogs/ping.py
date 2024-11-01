import discord
from discord.ext import commands
import time


class PingCog(commands.Cog, name="Ping Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Display the bot's ping.")
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("🏓 Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"{ctx.author.mention} 🏓 Pong! `{int(ping)} ms`")


async def setup(bot):
    await bot.add_cog(PingCog(bot))
