# 2b2t Priority queue discord bot announcer

## Commands

- !prioq -> Checks the priority queue length and sends it.
- !start -> Starts a loop that sends the status of the queue every 10 minutes. If it's equal to last one, it will not send anything, and instead log it in console.

## Install guide

Make sure to have at least [Python 3.9](https://www.python.org/downloads/) installed.

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

### TODO

[X] Coordinate conversion
[] ETA (with x bps, you'll reach y coords in z minutes)
[] Taxi Blacklist (Add, remove, view)