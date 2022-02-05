import asyncio
import json
import os
import sys
import nextcord
import qlogging
import requests
from colorama import Back, Fore, Style
from dotenv import load_dotenv
from nextcord.ext import commands, tasks

stats = requests.get("https://2bqueue.info/*").json()
bot = commands.Bot(command_prefix="!")

load_dotenv()


# Set the logging format and level. I am mad I didn't use the logging module before (or in this case, qlogging, for cool colors ;3).
logger = qlogging.get_logger(
    format_str="[%(asctime)s] [%(levelname)s] > %(message)s",
    level="info",
    loggingmode="manual",
    colors={
        "DEBUG": Fore.CYAN + Style.BRIGHT,
        "INFO": Fore.GREEN + Style.BRIGHT,
        "WARNING": Fore.YELLOW + Style.BRIGHT,
        "ERROR": Fore.RED + Style.BRIGHT,
        "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
    },
    format_date="%Y-%m-%d %H:%M:%S",
)


class CloseButton(nextcord.ui.View):
    def __init__(self, message: nextcord.Message):
        super().__init__()
        self.message = message

    @nextcord.ui.button(label="🗑️", style=nextcord.ButtonStyle.red)
    async def close_button(
        self, button: nextcord.Button, interaction: nextcord.Interaction
    ):
        await self.message.delete()


def readConfig():
    with open("config.json", "r", encoding="utf8") as jsonfile:
        config = json.load(jsonfile)
        logger.info("Config loaded.")
        return config


# Run this the first time the bot is started


def first_startup():
    config = readConfig()
    logger.info("First startup. Doing necessary things.")
    print("Please, send here the Channel ID for the updating message.")
    channel_id = input()
    user_ids = {"userids": []}
    # Set the Channel Id to the config file
    config["channel_id"] = channel_id
    config["user_ids"] = user_ids
    with open("config.json", "w", encoding="utf8") as jsonfile:
        jsonfile.write(json.dumps(config))


# On ready, do this.
@bot.event
async def on_ready():

    # Set the bot's activity and presence
    await bot.change_presence(
        status=nextcord.Status.do_not_disturb,
        activity=nextcord.Game(name="https://github.com/Ixogamer"),
    )

    config = readConfig()

    if not config["channel_id"]:
        first_startup()
    config = readConfig()
    try:
        channel_id = int(config["channel_id"])
        logger.debug("Channel ID: %s", channel_id)
    except Exception as e:
        logger.error("Error while reading the channel id: %s", e)
        sys.exit(1)

    logger.info("Logged in as %s", bot.user)
    channel = bot.get_channel(channel_id)
    logger.info("Detected Channel ID: %s", channel_id)

    # You have to make the message a variable so the ctx.edit() can use it. Without it, it doesn't have the correct context.
    message = await channel.send(
        embed=nextcord.Embed(
            title="The bot has been enabled.", description="Welcome!", color=0x008B02
        )
    )
    logger.info("Message sent to channel: %s", message.channel)
    await asyncio.sleep(5)
    embed = nextcord.Embed(
        title="Command List:", description="!prioq \n !start", color=0x5300EB
    ).set_footer(
        text="Remember that you can always invoke the command list using !help"
    )
    await message.edit(embed=embed, delete_after=5)
    logger.info("Message edited to: %s", message.id)


@bot.event
async def on_command_error(ctx, error):
    # message_to_send = await ctx.send(f"An error occured: {str(error)}")
    # await message_to_send.edit(view=CloseButton(message_to_send))

    logger.error(error)


@bot.command()
async def prioq(ctx):
    stats = requests.get("https://2bqueue.info/*").json()
    estimatedtime = requests.get("https://api.2b2t.dev/prioq").json()[2]
    clean_embed = nextcord.Embed(
        title="Scale of unplayability (0 - 100)",
        description=f'Normal:{stats["regular"]}\nPrio: {stats["prio"]}',
        color=0xFF00BF,
    ).set_footer(text=f"Estimated queue time: {estimatedtime}")
    message_to_send = await ctx.send(embed=clean_embed)
    await message_to_send.edit(view=CloseButton(message_to_send))
    logger.info("%s ran !prioq, sent embed.", ctx.author)


@bot.command()
async def pingme(ctx):
    users_to_ping = []
    if ctx.content.startswith("!pingme"):
        users_to_ping.append(ctx.author.id)
        await ctx.channel.send(
            f"{ctx.author.mention}. Your name has been added to the list, you will be pinged."
        )


@bot.command()
async def start(ctx):
    repeat_command.start(ctx)
    logger.info("Starting 10 minute countdown.")


@bot.command()
async def coords(ctx, coordx: float, coordz: float):
    overworld_coords_x = int(coordx * 8)
    overworld_coords_z = int(coordz * 8)
    nether_coords_x = int(coordx // 8)
    nether_coords_z = int(coordz // 8)
    embed = nextcord.Embed(title="Coordinates conversion result:")
    embed.set_author(name="Sponsored by Ccorp", url="https://discord.gg/ccorp")
    embed.add_field(
        name="Nether to Overworld:",
        value=f"**X:** {overworld_coords_x} | **Z:** {overworld_coords_z}",
        inline=False,
    )
    embed.add_field(
        name="Overworld to Nether:",
        value=f"**X:** {nether_coords_x} | **Z:** {nether_coords_z}",
        inline=False,
    )
    embed.set_footer(text="Made by GUMI#0727")
    message_to_send = await ctx.send(embed=embed)
    await message_to_send.edit(view=CloseButton(message_to_send))

    logger.info("Ran command coords with values: %s, %s", coordx, coordz)


@bot.command()
async def eta(ctx, blocks: int = 0, bps: float = 18.0):
    if blocks == 0:
        message_to_send = await ctx.send(
            "Usage: !eta [Blocks to travel] [Blocks per second] \n Example: `!eta 5000 18`. \n If the blocks per second isnt set, it will use the value 18."
        )
        await message_to_send.edit(view=CloseButton(message_to_send))
        return
    seconds = blocks / bps
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    result = f"%d:%02d:%02d" % (hour, minutes, seconds)
    embed = nextcord.Embed(title="Estimated time of arrival:")
    embed.set_author(name="Sponsored by Ccorp", url="https://discord.gg/ccorp")
    embed.add_field(
        name=f"Result at {bps} blocks per second:",
        value=f"{result} \n\n*(Hours:Minutes:Seconds)*",
        inline=False,
    )
    embed.set_footer(text="Made by GUMI#0727")
    message_to_send = await ctx.send(embed=embed)
    await message_to_send.edit(view=CloseButton(message_to_send))
    logger.info("Command eta was called with values: %s, %s", blocks, bps)


@bot.command()
async def banned(ctx, username):
    r = requests.get(f"https://api.cokesniffer.org/bans/?username={username}")
    if r.status_code == 200:
        clean_embed = nextcord.Embed(
            title="Banned list information:",
            description=f'User **{username}** is banned for rules: {r.json()["rules"]}',
            color=0xFF00BF,
        )
        message_to_send = await ctx.send(embed=clean_embed)
        await message_to_send.edit(view=CloseButton(message_to_send))
    else:
        clean_embed = nextcord.Embed(
            title="Banned list information:",
            description=f"User **{username}** is not banned.",
            color=0xFF00BF,
        )
        message_to_send = await ctx.send(embed=clean_embed)
        await message_to_send.edit(view=CloseButton(message_to_send))

    logger.info("%s ran !banned with username %s, sent embed.", ctx.author, username)


@bot.command()
async def muted(ctx, username):
    r = requests.get(f"https://api.cokesniffer.org/mutes/?username={username}")
    if r.status_code == 200:
        clean_embed = nextcord.Embed(
            title="Mute list information:",
            description=f'User **{username}** is **{r.json()["type"]}** muted for rules: **{r.json()["rules"]}**',
            color=0xFF00BF,
        )
        message_to_send = await ctx.send(embed=clean_embed)
        await message_to_send.edit(view=CloseButton(message_to_send))
    else:
        clean_embed = nextcord.Embed(
            title="Mute list information:",
            description=f"User **{username}** is not muted.",
            color=0xFF00BF,
        )
        message_to_send = await ctx.send(embed=clean_embed)
        await message_to_send.edit(view=CloseButton(message_to_send))

    logger.info("%s ran !muted with username %s, sent embed.", ctx.author, username)


@tasks.loop(minutes=10)
async def repeat_command(ctx):
    global stats
    old_stats = stats
    stats = requests.get("https://2bqueue.info/*").json()
    estimatedtime = requests.get("https://api.2b2t.dev/prioq").json()[2]

    if stats == old_stats:
        logger.info("%d is equal to old value. Skipping message.", stats["total"])
        return

    # if stats["prio"] == 0:
    #     user_id = '<@483056864355942405>'
    #     await ctx.channel.send(f'{user_id}')
    #     return

    clean_embed = nextcord.Embed(
        title="Scale of unplayability (0 - 100)",
        description=f'Normal:{stats["regular"]}\nPrio: {stats["prio"]}',
        color=0xFF00BF,
    ).set_footer(text=f"Estimated queue time: {estimatedtime}")

    await ctx.send(embed=clean_embed)
    logger.info(
        "Message sent with value %d, %d, %d. Wating 10 minutes.",
        stats["prio"],
        stats["regular"],
        stats["total"],
    )


bot.run(os.getenv("TOKEN"))
