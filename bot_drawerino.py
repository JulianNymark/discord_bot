#!/bin/bash/python3.5

import discord
import logging

logging.basicConfig(level=logging.INFO)

###########################
# DISCORDERINO
###########################

token = os.environ['DISCORD_SECRET_TOKEN']
client = discord.Client()
