import discord
import asyncio
import os
import logging
import threading
import shutil

from flask import Flask, request
from passlib.hash import sha512_crypt

# logging.basicConfig(level=logging.DEBUG,
#                     format='(%(threadName)-10s) %(message)s'
# )

meme_queue = []
meme_lock = threading.Condition()
meme_directory = './temp'

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
        meme_lock.acquire()
        meme_lock.wait()
        meme = meme_queue.pop()
        with open(meme_directory + '/' + meme.filename, 'rb') as f:
            await client.send_file(channel_by_name('memes'), f)
        meme_lock.release()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    update_channels()

def discorderino():
    client.loop.create_task(my_background_task())
    client.run(token)

threading.Thread(target=discorderino).start()

###########################
# FLASKERINO
###########################

app = Flask(__name__)
hash = sha512_crypt.hash(os.environ['DISCORD_UPLOAD_PASSWORD'])

@app.route('/draws', methods=['POST'])
def draw():
    try:
        file = request.files['file']
    except:
        return '{ success : failure }'

    try:
        password = request.form['password']
    except:
        return '{ success : failure }'

    if not sha512_crypt.verify(password, hash):
        return '{ success : failure }'

    if file:
        shutil.rmtree(meme_directory, ignore_errors=True)
        if not os.path.exists(meme_directory):
            os.mkdir(meme_directory)

        file.save(os.path.join(meme_directory, file.filename))

        meme_lock.acquire()
        meme_queue.append(file)
        meme_lock.notify()
        meme_lock.release()
        return '{ success : success }'
    return '{ success : failure }'

def flaskerino():
    if __name__ == '__main__':
        app.run()


threading.Thread(target=flaskerino).start()

# :poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop:
