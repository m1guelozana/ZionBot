import discord
from discord.ext import commands
import hashlib
import itertools
import string
import concurrent.futures

class HashCrackerCog(commands.Cog, name="Hash Cracker Command"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.passwords = {}
        self.characters = string.ascii_letters + string.digits  # Limitar a caracteres comuns

    async def load_dictionary(self):
        algorithms = ["md5", "sha1", "sha256", "sha384", "sha512"]
        with open("passwords.txt", "r", encoding="utf-8") as file:
            for line in file:
                password = line.strip()
                self.passwords[password] = {
                    algo: self.hash_function(password, algo) for algo in algorithms
                }

    def hash_function(self, password, algorithm):
        hash_func = getattr(hashlib, algorithm)
        return hash_func(password.encode()).hexdigest()

    def detect_algorithm(self, hash_value):
        hash_length = len(hash_value)
        if hash_length == 32: 
            return "md5"
        elif hash_length == 40:
            return "sha1"
        elif hash_length == 64:
            return "sha256"
        elif hash_length == 96:
            return "sha384"
        elif hash_length == 128:
            return "sha512"
        else:
            return None

    async def brute_force(self, hash_value, max_length=4):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_attempt = {
                executor.submit(self.try_passwords, length, hash_value): length
                for length in range(1, max_length + 1)
            }
            for future in concurrent.futures.as_completed(future_to_attempt):
                if found_password := future.result():
                    return found_password
        return None

    def try_passwords(self, length, hash_value):
        for attempt in itertools.product(self.characters, repeat=length):
            password = ''.join(attempt)
            for algo in ["md5", "sha1", "sha256", "sha384", "sha512"]:
                if self.hash_function(password, algo) == hash_value:
                    return password
        return None

    @commands.command(name="hashcracker", description="Cracks a given hash. If a password is not found, it will try brute force. (Only works with 4 characters length)")
    async def hash_cracker(self, ctx, hash_value: str, max_length: int = 4):
        algorithm = self.detect_algorithm(hash_value)
        if not algorithm:
            await ctx.send("Algorith not supported")
            return

        for password, hashes in self.passwords.items():
            if hashes.get(algorithm) == hash_value:
                await ctx.send(f"{ctx.author.mention}`{hash_value}`:`{password}` using: `{algorithm}`.")
                return

        await ctx.send(f"{ctx.author.mention}! Unmasking.")
        found_password = await self.brute_force(hash_value, max_length)
        if found_password:
            await ctx.send(f"{ctx.author.mention} `{hash_value}`: `{found_password}` using: `{algorithm}`.")
        else:
            await ctx.send(f"{ctx.author.mention} Impossible to unmask: `{hash_value}`")

async def setup(bot: commands.Bot):
    cog = HashCrackerCog(bot)
    await cog.load_dictionary()
    await bot.add_cog(cog)
