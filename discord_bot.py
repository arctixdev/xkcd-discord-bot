from http.client import ResponseNotReady
from multiprocessing.util import get_temp_dir
from optparse import Option
from ssl import Options
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random, json, requests, os

load_dotenv()
url = "https://xkcd.com/"
TOKEN = os.getenv("TOKEN")
bot = commands.Bot()

number_option = discord.Option(
    int,
    "The specific comic to send",
    name="number",
    type=int,
    default=False,
    input_type=int,
    required=False,
    min_value=1,
    max_value=3000,
)

command_options = [number_option]


def random_comic_number():
    max = current_comic_number()
    number = random.randint(1, max)
    return number


def current_comic_number():
    return int(json.loads(requests.get("https://xkcd.com/info.0.json").text)["num"])


def get_info(number):
    info = requests.get(f"{url}{number}/info.0.json").text
    info_loaded = json.loads(info)
    return info_loaded


def get_embed(number):
    comic = get_info(number)
    img_url = comic["img"]
    embed = discord.Embed(
        title=comic["title"],
        description=f"Link to comic: {url}{number}/",
        color=discord.Colour.dark_purple(),
    )
    embed.set_image(url=img_url)
    # embed.add_field(False,"h","h")
    return embed


@bot.slash_command(
    name="comic", description="Return a XKCD comic", Options=command_options
)
async def get_comic(ctx, numberopt=number_option):
    number = random_comic_number()
    if numberopt:
        try:
            number = int(numberopt)  # type: ignore
            if number > 0 and number < current_comic_number():
                pass
            else:
                await ctx.respond(
                    f"Comic number must be empty for random or between 1 and {current_comic_number()}"
                )
                return
        except:
            await ctx.respond("ERROR... Option must be empty or a number")
            return
    embed = get_embed(number)
    await ctx.respond(embed=embed)


@bot.slash_command(name="info", description="Show info")
async def info(ctx):
    await ctx.respond(
        """
    This bot is made by @Un1ocked_#0284
    It show comics from https://xkcd.com/ made by Randall Munroe
    Usage:
        /comic      For a random comic
        /comic x   For comic number x
    """
    )


bot.run(TOKEN)
