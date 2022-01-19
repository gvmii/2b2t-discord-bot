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

Made with [Pycord](https://github.com/Pycord-Development/pycord)
