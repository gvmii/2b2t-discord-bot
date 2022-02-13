import asyncio
import json
import os
import sys
import nextcord
import aiohttp
import aiofiles
from rich import print, console
from dotenv import load_dotenv
from nextcord.ext import commands, tasks

bot = commands.Bot(
    command_prefix="!",
    status=nextcord.Status.do_not_disturb,
    activity=nextcord.Game(name="https://github.com/Ixogamer"),
)
console = console.Console()
load_dotenv()


class CloseButton(nextcord.ui.View):
    def __init__(self, message: nextcord.Message):
        super().__init__()
        self.message = message

    @nextcord.ui.button(label="🗑️", style=nextcord.ButtonStyle.red)
    async def close_button(
        self, button: nextcord.Button, interaction: nextcord.Interaction
    ):
        await self.message.delete()


async def readConfig():
    async with aiofiles.open("config.json", "r", encoding="utf8") as jsonfile:
        config = json.loads(await jsonfile.read())
        console.log("Config loaded [green]successfully[/green].")
        return config


# Run this the first time the bot is started


async def first_startup():
    config = await readConfig()
    console.log("Starting...")

    print("Please, send here the Channel ID for the updating message.")
    channel_id = input()
    # user_ids = {"userids": []}
    # Set the Channel Id to the config file
    config["channel_id"] = channel_id
    # config["user_ids"] = user_ids
    async with aiofiles.open("config.json", "w", encoding="utf8") as jsonfile:
        await jsonfile.write(json.dumps(config))


# On ready, do this.
@bot.event
async def on_ready():
    config = await readConfig()
    if not config["channel_id"]:
        await first_startup()
        config = await readConfig()
    try:
        channel_id = int(config["channel_id"])
        console.log(f"Channel ID Set to: {channel_id}.")
    except Exception as e:
        console.log(f"[red]Error[/red]: Couldn't read channel id: {e}")
        sys.exit(1)

    print(f"Logged in as {bot.user}.")
    channel = bot.get_channel(channel_id)
    console.log(f"Channel #{channel.name} ({channel.id}) [green]found[/green].")

    # You have to make the message a variable so the ctx.edit() can use it. Without it, it doesn't have the correct context.
    message = await channel.send(
        embed=nextcord.Embed(
            title="The bot has been enabled.", description="Welcome!", color=0x008B02
        )
    )
    await asyncio.sleep(5)
    embed = nextcord.Embed(
        title="Command List:", description="!prioq \n !start", color=0x5300EB
    ).set_footer(
        text="Remember that you can always invoke the command list using !help"
    )
    await message.edit(embed=embed, delete_after=5)


@bot.event
async def on_command_error(ctx, error):
    console.log(f"[red]Error[/red]: {str(error)}")


@bot.command()
async def queue(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://2bqueue.info/*") as response:
            stats = await response.json()
        async with session.get("https://api.2b2t.dev/prioq") as response:
            estimatedtime = await response.json()
            estimatedtime = estimatedtime[2]
    clean_embed = nextcord.Embed(
        title="Scale of unplayability (0 - 100)",
        description=f'Normal:{stats["regular"]}\nPrio: {stats["prio"]}',
        color=0xFF00BF,
    ).set_footer(text=f"Estimated queue time: {estimatedtime}")
    message_to_send = await ctx.send(embed=clean_embed)
    await message_to_send.edit(view=CloseButton(message_to_send))


@bot.command()
async def start(ctx):
    repeat_command.start(ctx)


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


@bot.command()
async def user(ctx, username):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.mojang.com/users/profiles/minecraft/{username}"
        ) as response:
            data = await response.json()
            uuid = data["id"]

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://api.cokesniffer.org:8080/mutes?username={username}"
        ) as response:
            # I have to do this because the API is scuffed and returns plain text.
            # FIXME: Fix this if the API is fixed.
            code = response.status
            data = await response.read()
            loaded_data = json.loads(data)
    if code == 200:
        is_muted = True
        mute_type = loaded_data["type"]
        mute_rules = loaded_data["rules"]
    else:
        is_muted = False

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://api.cokesniffer.org:8080/bans?username={username}"
        ) as response:
            code = response.status
            data = await response.read()
            loaded_data = json.loads(data)
    if code == 200:
        is_banned = True
        ban_rules = loaded_data["rules"]
    else:
        is_banned = False

    clean_embed = nextcord.Embed(
        title=f"Results for lookup of player {username}: ", color=0x008B02
    )
    clean_embed.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}?size=64.png")
    clean_embed.add_field(
        name="Banned:",
        value=f"**{is_banned}**, for rule(s) **{ban_rules}**",
        inline=True,
    )
    clean_embed.add_field(
        name="Muted:",
        value=f"**{is_muted}**, of type **{mute_type}**, for rules **{mute_rules}**",
        inline=True,
    )
    message_to_send = await ctx.send(embed=clean_embed)
    await message_to_send.edit(view=CloseButton(message_to_send))


@tasks.loop(minutes=10)
async def repeat_command(ctx):
    global stats
    old_stats = stats
    async with aiohttp.ClientSession() as session:
        async with session.get("https://2bqueue.info/*") as response:
            stats = await response.json()
        async with session.get("https://api.2b2t.dev/prioq") as response:
            estimatedtime = await response.json()
            estimatedtime = estimatedtime[2]

    if stats == old_stats:
        console.log("[yellow]No change in stats[/yellow], skipping.")
        return

    clean_embed = nextcord.Embed(
        title="Scale of unplayability (0 - 100)",
        description=f'Normal:{stats["regular"]}\nPrio: {stats["prio"]}',
        color=0xFF00BF,
    ).set_footer(text=f"Estimated queue time: {estimatedtime}")
    await ctx.send(embed=clean_embed)


bot.run(os.getenv("TOKEN"))
