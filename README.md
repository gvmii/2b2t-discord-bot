# 2b2t Priority queue discord bot announcer

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Commands

- !queue -> Checks the queue length and sends it.
- !start -> Starts a loop that sends the status of the queue every 10 minutes. If it's equal to last one, it will not send anything, and instead log it in console.
- !banned [USERNAME] -> Checks if an user is banned in 2b2t.
- !muted [USERNAME] -> Checks if an user is muted in 2b2t.
- !eta [BLOCKS] [BPS] -> Calculates how long you would take to travel x blocks in y bps
- !coords [X COORD] [Z COORD] -> Converts Overworld coordinates to Netherrack and viceversa

## Install guide

Make sure to have at least [Python 3.10](https://www.python.org/downloads/) installed.

1. Open `.env` and add your bot token.
2. Run the following commands in a terminal in the same directory:

```bash
$ pip install -r requirements.txt
$ python ./bot.py
```

## Credits

Made with [Nextcord](https://github.com/nextcord/nextcord/)

### API's

[2bqueue.info](https://2bqueue.info/) from [Tycrek](https://tycrek.com/)
[2b2t.dev](https://api.2b2t.dev/)
[cokesniffer.org](https://api.cokesniffer.org) for bans and mute info.

### TODO

Feel free to ask for a module GUMI#0727
