import json
from locale import format_string
import os
from datetime import datetime
from time import sleep
import discord
import requests
import qlogging
import asyncio
from colorama import Fore, Back, Style
from discord.ext import commands, tasks
from dotenv import load_dotenv

stats = requests.get('https://api.2b2t.dev/prioq').json()
client = discord.Client(prefix='!')

load_dotenv()

# Pretty crazy stuff how there's literally a module for this and more.

# def logging.DEBUG(message_to_format):
#     unix_timestamp = datetime.now().timestamp()
#     converted_timestamp = datetime.fromtimestamp(int(unix_timestamp))
#     print(f"[{converted_timestamp.strftime('%d-%m-%y %H:%M:%S')}] {message_to_format}")

# def logError(message_to_format, doExit):
#     init() #Initialize colorama
#     sys.stderr.write(f"{Fore.RED}An error ocurred with message: {message_to_format}{Style.RESET_ALL}")
#     if doExit:
#         sys.exit(1)

#TODO: Add presence for the bot

# Set the logging format and level. I am mad I didn't use the logging module before (or in this case, qlogging, for cool colors ;3).
logger = qlogging.get_logger(format_str='[%(asctime)s] [%(levelname)s] > %(message)s', level='info', loggingmode="manual", colors=
                            {
                            'DEBUG': Fore.CYAN + Style.BRIGHT,
                            'INFO': Fore.GREEN + Style.BRIGHT,
                            'WARNING': Fore.YELLOW + Style.BRIGHT,
                            'ERROR': Fore.RED + Style.BRIGHT,
                            'CRITICAL': Fore.RED + Back.WHITE + Style.BRIGHT,
                        }, format_date='%Y-%m-%d %H:%M:%S')




def readConfig():
    with open('config.json', 'r') as jsonfile:
        config = json.load(jsonfile)
        logger.info('Config loaded.')
        jsonfile.close()
        return config

# Run this the first time the bot is started
def first_startup():
    config = readConfig()
    logger.info('First startup. Doing necessary things.')
    print('Please, send here the Channel ID for the updating message.')
    channel_id=input()
    # Set the Channel Id to the config file
    config['channel_id'] = channel_id
    with open('config.json', 'w') as jsonfile:
        json.dump(config, jsonfile)
        jsonfile.close()


# On ready, do this.
@client.event
async def on_ready():
    config = readConfig()
    
    if not config['channel_id']:
        first_startup()
    config = readConfig()
    try:
        channel_id = int(config['channel_id'])
    except Exception as e:
        logger.error(f'Error while reading the channel id: {e}')
        exit(1)

    logger.info(f'Logged in as {client.user}')
    channel = client.get_channel(channel_id)
    logger.info(f'Detected Channel ID: {channel_id}')
    
    # You have to make the message a variable so the ctx.edit() can use it. Without it, it doesn't have the correct context.
    message = await channel.send(embed=discord.Embed(title='The bot has been enabled.', description='Welcome!', color=0x008b02))
    logger.info(f'Message sent to channel: {message.channel}')
    await asyncio.sleep(5)
    embed = discord.Embed(title='Command List:', description='!prioq \n !start', color=0x5300eb).set_footer(text='Remember that you can always invoke the command list using !help')
    await message.edit(embed=embed, delete_after=5)
    logger.info(f'Message edited to: {message.id}')



@client.event
async def on_message(ctx):

    if ctx.author == client.user:
        return

    if ctx.content.startswith('!prioq'):
        stats = requests.get('https://api.2b2t.dev/prioq').json()
        estimatedtime = stats[2]
        clean_embed = discord.Embed(title='Scale of unplayability (0 - 100)', description=stats[1], color=0xff00bf).set_footer(text=f'Estimated queue time: {estimatedtime}')
        await ctx.channel.send(embed=clean_embed)
        logger.info(f'{ctx.author} ran !prioq, sent embed.')

    if ctx.content.startswith('!start'):
        repeat_command.start(ctx)
        logger.info('Starting 10 minute countdown.')

@tasks.loop(minutes = 10)
async def repeat_command(ctx):
    global stats
    old_stats = stats
    stats = requests.get('https://api.2b2t.dev/prioq').json()
    estimatedtime = stats[2]
    
    if stats == old_stats:
        logger.info(f'{stats[1]} is equal to old value. Skipping message.')
        return
    
    if stats[1] == 0:
        user_id = '<@483056864355942405>'
        await ctx.channel.send(f'{user_id}')
        return

    clean_embed = discord.Embed(title='Scale of unplayability (0 - 100)', description=stats[1], color=0xff00bf).set_footer(text=f'Estimated queue time: {estimatedtime}')
    await ctx.channel.send(embed=clean_embed)

    logger.info(f'Message sent with value {stats[1]}, wating 10 minutes.')



client.run(os.getenv('TOKEN'))
