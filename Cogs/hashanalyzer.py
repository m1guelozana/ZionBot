import discord
import hashlib

from discord.ext import commands

class HashAnalyzerCog(commands.Cog, name="Hash AnalyzerCommand"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="analyzehash", description="Analyzes a given hash.")
    async def hash_analyze(self, ctx, hash_value: str):
        
        hash_types = {
            32: "MD5",
            40: "SHA-1",
            56: "SHA-226",
            64: "SHA-256",
            96: "SHA-384",
            128: "SHA-512",
        }
        
        hash_length = len(hash_value)
        
        if hash_length == 60 and hash_value.startswith(("$2a$", "$2b$", "$2y$")):
            hash_type = "bcrypt"
        else:
            hash_type = hash_types.get(hash_length, "Unknown hash type")

        await ctx.send(
            f"{ctx.author.mention} type:{hash_type}"
        )

async def setup(bot: commands.Bot):
  await bot.add_cog(HashAnalyzerCog(bot))