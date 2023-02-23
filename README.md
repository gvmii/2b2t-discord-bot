# 2b2t utility Discord bot

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

Missing something? Feel free to ask for a module GUMI#1337

This repository is mostly a learning experience for me, so please, if you see something wrong, open a pull request.

---

## Commands

- !queue -> Checks the queue length and sends it.
- !start -> Starts a loop that sends the status of the queue every 10 minutes. If it's equal to last one, it will not send anything, and instead log it in console.
- !user [USER] -> Checks mute/ban status [NOT WORKING, API DELETED] on 2b2t, sends skin info, will do more things.
- !eta [BLOCKS] [BPS] -> Calculates how long you would take to travel x blocks in y bps
- !coords [X COORD] [Z COORD] -> Converts Overworld coordinates to Nether and viceversa

## Install guide
Make sure to have at least [Python 3.10](https://www.python.org/downloads/) installed.
Go to [discord.com](https://discord.com/developers/applications)
1. Create a New Application
2. Go to the bot tab, Click on add bot
3. Enable These Settings in Privileged Gateway Intents Category: Presence Intent, Server Members Intent,
Message Content Intent
4. Add the bot to your server
5.  Open `.env` and add your bot token.
6. Run the following commands in a terminal in the same directory:

```bash
py -m pip install -r requirements.txt
py ./bot.py
```

## Credits

Made with [Nextcord](https://github.com/nextcord/nextcord/)

### API's

- **[2bqueue.info](https://2bqueue.info/)** from [Tycrek](https://tycrek.com/)

- **[2b2t.dev](https://api.2b2t.dev/)**

- **[cokesniffer.org](https://api.cokesniffer.org)** for bans and mute info.

- **[crafatar.com](https://crafatar.com/)** for skin info

- **[Mojang API](https://mojang-api-docs.netlify.app/)** for UUID conversion.

### TODO

- Add utlity Cogs
