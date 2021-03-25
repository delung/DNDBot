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

#Usage message for dice roll
async def help(message):
	await message.channel.send('Ex: $r1d20')

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	#Specific regex match for rolls.
	#Format is $r, then a number from 1-9, then any amount of numbers from 0-9.
	#After that is d
	#Then it is followed by again, 1-9 and any amount of 0-9. 
	#The $ at the end means there must not be anything after the numbers.
	roll_regex = re.compile(r"\$r[1-9][0-9]*d[1-9][0-9]*$")
	#Match to $help XXX where XXX is any alphanumeric string.
	help_regex = re.compile(r"\$help \w*$")
	if message.author == client.user:
		return
	elif message.content == "$help":
		help_msg = await get_help("help")
		await message.channel.send(message.author.mention + "\n" + help_msg)
	#Message matched roll regex
	elif not roll_regex.match(message.content) is None: 
		await Rolling.make_roll(message)
	elif message.content.lower() == '$hello':
		await message.channel.send('https://tenor.com/view/howdy-cowboy-woody-toy-story-shark-gif-5543642')
	elif not help_regex.match(message.content) is None:
		#since the message is always $help XXX (confirmed by regex), skip the first 6 characters.
		help_msg = await get_help(help_regex.match(message.content).group()[6:])
		await message.channel.send(message.author.mention + "\n" + help_msg)
	elif message.content.lower() == '$ree':
		await message.channel.send(get_ree_gif())
	elif message.content.lower() == '$ricardo':
		await message.channel.send(get_ricardo_gif())
	elif message.content.lower() == '$debug method':
		await message.channel.send(embed=Rolling.print_help_embedded())
  


#db example
#set_value(1,20)
#print(get_value(1))


if __name__ == "__main__":
	#keep_alive()
	req = requests.get("https://discord.com/api/v8/gateway")
	print(req.headers)
	client.run(os.getenv("DISCORD_BOT_TOKEN"))
	print("Exiting")
