import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = commands.Bot()

@bot.slash_command(name="random")
async def first_slash(ctx): 
    await ctx.respond("You executed the slash command!")

bot.run(TOKEN)

