import json
import os
from datetime import datetime
from time import sleep
import discord
import requests
from discord.ext import tasks, commands
from dotenv import load_dotenv

stats = requests.get('https://api.2b2t.dev/prioq').json()
client = discord.Client(prefix='!')

load_dotenv()

def logger(message_to_timestamp):
    unix_timestamp = datetime.now().timestamp()
    converted_timestamp = datetime.fromtimestamp(int(unix_timestamp))
    print(f"[{converted_timestamp.strftime('%d-%m-%y %H:%M:%S')}] {message_to_timestamp}")

def readConfig():
    with open('config.json', 'r') as jsonfile:
        config = json.load(jsonfile)
        logger('Config loaded.')
        jsonfile.close()
        return config

# Run this the first time the bot is started
def first_startup():
    config = readConfig()
    logger('First startup. Doing necessary things.')
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
    channel_id = int(config['channel_id'])

    logger(f'We have logged in as {client.user}')
    channel = client.get_channel(channel_id)
    logger(f'Detected Channel ID: {channel_id}')
    
    # You have to make the message a variable so the ctx.edit() can use it. Without it, it doesn't have the correct context.
    message = await channel.send(embed=discord.Embed(title='The bot has been enabled.', description='Welcome!', color=0x008b02))
    logger(f'Message sent to channel: {message.id}')
    sleep(5)
    embed = discord.Embed(title='Command List:', description='!prioq \n !start', color=0x5300eb).set_footer(text='Remember that you can always invoke the command list using !help')
    await message.edit(embed=embed, delete_after=5)
    logger(f'Message edited to: {message.id}')



@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('!prioq'):
        stats = requests.get('https://api.2b2t.dev/prioq').json()
        clean_embed = discord.Embed(title='Scale of unplayability (0 - 100)', description=stats[1], color=0xff00bf).set_footer(text='L9 Gumi got ratted making this')
        await message.channel.send(embed=clean_embed)
        logger(f'{message.author} ran !prioq, sent embed.')
    if message.content.startswith('!start'):
        repeat_command.start(message)
        logger('Starting 10 minute countdown.')

@tasks.loop(minutes = 10)
async def repeat_command(message):
    global stats
    old_stats = stats
    stats = requests.get('https://api.2b2t.dev/prioq').json()
    
    if stats == old_stats:
        logger(f'{stats[1]} is equal to old value. Skipping message.')
        return 
    
    clean_embed = discord.Embed(title='Scale of unplayability (0 - 100)', description=stats[1], color=0xff00bf).set_footer(text='L9 Gumi got ratted making this')
    await message.channel.send(embed=clean_embed)
    logger(f'Message sent with value {stats[1]}, wating 10 minutes.')



client.run(os.getenv('TOKEN'))