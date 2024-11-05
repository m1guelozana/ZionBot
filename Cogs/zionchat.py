import discord
import os
import dotenv
import cohere
from discord.ext import commands

dotenv.load_dotenv()

cohere_api_key = os.getenv("cohere_token")
co = cohere.Client(cohere_api_key)

class ChatBot(commands.Cog, name="ChatBot using Cohere"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def generate_response(self, prompt):
        try:
            response = co.generate(
                model='command-r-08-2024',
                prompt=prompt,
                max_tokens=300,
                temperature=0.7,
            )
            return response.generations[0].text.strip()
        except Exception as e:
            return f"Error calling Cohere API: {str(e)}"

    @commands.command(name="chat", description="Interact with the chatbot")
    async def chat(self, ctx, *, prompt: str):
        response = self.generate_response(prompt)
        await ctx.send(response)

async def setup(bot: commands.Bot):
    cog = ChatBot(bot)
    await bot.add_cog(cog)
