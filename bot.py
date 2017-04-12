import discord
from discord.ext import commands
import random
import os

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)

channel_list = []

def random_channel():
    return random.choice(channel_list)

def update_channels():
    global channel_list
    channel_list = list(bot.get_all_channels())

def setup():
    global channel_list
    channel_list = list(bot.get_all_channels())

    print('channels:')
    for i in channel_list:
        print(' - ' + i.name)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    setup()

@bot.event
async def on_member_join(member):
    await bot.send_message(random_channel(), 'HIHIHI YOU, YOU... ' + member.nick + ' YOU! YOU\'RE THE BEST!!!! STAY FOREVER!!')

@bot.event
async def on_member_remove(member):
    await bot.send_message(random_channel(), 'RIP in pepperonis... ' + member.nick)

@bot.event
async def on_member_update(before, after):
    print("before", before)
    print('after', after)
    #await bot.send_message(random_channel(), '{} you smell different! that\'s nice!'.format(after))

@bot.event
async def on_channel_create(channel):
    await bot.send_message(channel, 'NEW CHANNEL NEW CHANNEL NEW CHANNEL!')
    await bot.send_message(channel, 'dis ma litterbox!!! :poop: :poop:')
    await bot.send_message(channel, ':poop:')
    await bot.send_message(channel, ':poop:')
    update_channels()

@bot.event
async def on_channel_delete(channel):
    await bot.send_message(random_channel(), 'RIP, '+ channel.name + '. That channel was a piece of shit!')
    update_channels()

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

# @bot.command()
# async def repeat(times : int, content='repeating...'):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at} :poop:'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

token = os.environ['DISCORD_SECRET_TOKEN']
bot.run(token)
