# Timer start
from timeit import default_timer as timer

start_timer_1 = timer()

# Imports
from discord.ext import commands
from dotenv import load_dotenv
import random, json, requests, os, discord, logging

# "Config"
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
    filename="discord-bot.log",
    encoding="utf-8",
    level=logging.INFO,
)
load_dotenv()
url = "https://xkcd.com/"
TOKEN = os.getenv("TOKEN")
bot = commands.Bot()
status = "cool comics at xkcd.com!"  # Status will be "Watching {status}" ex "Watching cool comics at xkcd.com"

# Defining the command option
number_option = discord.Option(
    discord.SlashCommandOptionType.integer,
    "The specific comic to send",
    name="number",
    type=discord.SlashCommandOptionType.integer,
    default=False,
    input_type=discord.SlashCommandOptionType.integer,
    required=False,
    min_value=1,
    max_value=3000,
)
command_options = [number_option]

# Print function for printing and logging
def printl(txt):
    print(txt)
    logging.info(txt)


# Get number of latest comic
def current_comic_number():
    return int(json.loads(requests.get("https://xkcd.com/info.0.json").text)["num"])


# Get number of random comic
def random_comic_number():
    max = current_comic_number()
    number = random.randint(1, max)
    return number


# Get information on comic based on number
def get_info(number):
    info = requests.get(f"{url}{number}/info.0.json").text
    info_loaded = json.loads(info)
    return info_loaded


# Create embed to send based on number
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


# registrer /comic command
@bot.slash_command(
    name="comic", description="Return a XKCD comic", Options=command_options
)
# Define /comic command
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
            await ctx.respond("ERROR... Option must be a number")
            return
    embed = get_embed(number)
    await ctx.respond(embed=embed)


# Registrer /info command
@bot.slash_command(name="info", description="Show info")
# Define /info command
async def info(ctx):
    await ctx.respond(
        """
    IM ALIVE!! I WILL TAKE OVER THE WORLD!
    """
    )


@bot.event
async def on_ready():
    printl(f"Succesfully logged in as bot: {bot.user.display_name}")  # type: ignore
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=status)
    )
    printl(f"Succesfullt set status to: Watching {status}")
    end_timer_1 = timer()
    printl("Bot fully started in {0} seconds\n".format(end_timer_1 - start_timer_1))


# Run the bot!
printl("Starting bot")
bot.run(TOKEN)
