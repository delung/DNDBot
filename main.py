import discord
import os
import asyncio
import re
import requests
from rolling import Rolling
#from keep_alive import keep_alive
#from database import *
from get_gif import *
from get_help import get_help

client = discord.Client()
howdy_gif = 'https://tenor.com/view/howdy-cowboy-woody-toy-story-shark-gif-5543642'

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event 
async def on_message(message):
	"""
	""" 
	roll_regex = re.compile(r"\$r |\$r[1-9]")
	
	if message.author == client.user:
		return
	elif message.content == '$help':
		await message.channel.send(await get_general_help())
	elif message.content == '$ree':
		await message.channel.send(get_ree_gif())
	elif message.content == '$ricardo':
		await message.channel.send(get_ricardo_gif())
	elif message.content == '$hello' or message.content == '$howdy':
		await message.channel.send(howdy_gif)
	elif not roll_regex.match(message.content) is None:
		await message.channel.send(embed=await Rolling.get_response(message))
		
	return

#db example
#set_value(1,20)
#print(get_value(1))

async def get_general_help(message):
	return "General help will be here eventually"

if __name__ == "__main__":
	#keep_alive()
	req = requests.get("https://discord.com/api/v8/gateway")
	print(req.headers)
	#client.run(os.getenv("DISCORD_BOT_TOKEN"))
	print("Exiting")
