import discord
import asyncio
import os
import logging
import threading

from flask import Flask

# logging.basicConfig(level=logging.DEBUG,
#                     format='(%(threadName)-10s) %(message)s'
# )

meme_queue = []

###########################
# DISCORDERINO
###########################

token = os.environ['DISCORD_SECRET_TOKEN']
client = discord.Client()

channels = []

def update_channels():
    global client
    global channels
    channels=list(client.get_all_channels())

def channel_by_name(name):
    update_channels()
    for c in channels:
        if c.name == name:
            return c
    return None

async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed:
        if not meme_queue:
            await asyncio.sleep(0.5)
        else:
            meme = meme_queue.pop()
            await client.send_message(channel_by_name('memes'), meme)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def discorderino():
    client.loop.create_task(my_background_task())
    client.run(token)

threading.Thread(target=discorderino).start()

###########################
# FLASKERINO
###########################

app = Flask(__name__)

@app.route("/draw", methods=['POST'])
def draw():
    # receive body = image data -> client.send_image()
    meme_queue.append('a meme')
    return "{ success : failure }"

def flaskerino():
    if __name__ == "__main__":
        app.run()


threading.Thread(target=flaskerino).start()
