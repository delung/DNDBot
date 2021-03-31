import discord
import os
import asyncio
import re
import requests
from rolling import Rolling
#from database import *
from battlemap import Battlemap
from char_sheet import Char_sheet
from get_gif import *

client = discord.Client()
howdy_gif = 'https://tenor.com/view/howdy-cowboy-woody-toy-story-shark-gif-5543642'

#TODO:
#Dictionary that maps discord id -> Player instance
players = dict()
bm = None

@client.event
async def on_ready():
	#TODO:
	#players = load_players() #Reads locally saved file into player instances
	#client.loop.create_task(create_backups()) #sets up hourly backups
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_disconnect():
	#TODO:
	#Maybe save players to file. I don't want to deal with conflicts
	#where the file is already open for the hourly update
	#so maybe just accept hourly backups only?
	pass

@client.event
async def on_message(message):
	"""
	"""
	roll_regex = re.compile(r"\$r |\$r[0-9]|\$roll[0-9]|\$roll|\$roll help")
	#TODO:
	player_regex = re.compile(r"") # Checks if the message is related to player
	map_regex = re.compile(r"\$map[a-z]+|\$map |\$maphelp|\$mapnew [0-9]+,[0-9]+")
	# checks if message is from channel
	if message.channel.type == discord.ChannelType.text:
		if message.author == client.user:
			return
		elif message.content == '$help':
			await message.channel.send(await get_general_help(message))
		elif message.content == '$ree':
			await message.channel.send(get_ree_gif())
		elif message.content == '$ricardo':
			await message.channel.send(get_ricardo_gif())
		elif message.content == '$hello' or message.content == '$howdy':
			await message.channel.send(howdy_gif)
		elif message.content == '$form':
			user = message.author
			await user.send(embed=await Char_sheet.get_response(message))
			await message.channel.send('Form sent to DMs')
		elif not roll_regex.match(message.content) is None:
			await message.channel.send(embed=await Rolling.get_response(message))
		elif not map_regex.match(message.content) is None:
			await message.channel.send(embed=await deal_with_map_message(message))
		elif not player_regex.match(message.content) is None:
			#TODO:
			#await deal_with_player_message(message)
			pass
	# checks if message is private
	elif message.channel.type == discord.ChannelType.private:
		if message.author == client.user:
			return
		elif message.content == '$form':
			await message.channel.send('DM recieved ;)')
	return

async def get_general_help(message: discord.Message) -> discord.Embed:
	return "General help will be here eventually"

async def deal_with_map_message(message: discord.Message) -> discord.Embed:
	global bm
	MAX_ROWS_TIMES_COLS = 27
	map_regex = re.compile(r"\$map[a-z]+|\$map |\$maphelp")
	new_map_regex = re.compile(r"\$mapnew [0-9]+,[0-9]+")
	if not new_map_regex.match(message.content) is None:
		nums = re.findall(r"[0-9]+", message.content)
		if int(nums[0]) * int(nums[1]) > MAX_ROWS_TIMES_COLS:
			return await Battlemap.get_usage_message(message)
		bm = Battlemap(int(nums[0]), int(nums[1]))
		return await bm.get_grid()
	elif not map_regex.match(message.content) is None:
		return await bm.get_response(message)

async def deal_with_player_message(message: discord.Message) -> discord.Embed:
	#TODO:
	"""
	Pseudocode:

	if msg == $new char:
		send_help_form_to_player_in_dm()
	if msg.channel is a DM and msg == filled_player_form:
		players[discord_id] = Player(msg)
	else:
		await message.channel.send(embed = await Player.get_response(message))
	"""
	pass

async def create_backups():
	#TODO:
	#while not client.is_closed:
		#asyncio.sleep(3600) #wait one hour
		#save_players_to_file()
		#OPTIONAL:
			#if num_files > 100:
				#delete oldest file
	pass

async def save_players_to_file():
	#TODO:
	"""
	Pseudo code:
	change_file_name("players.json", "players_old_DATEANDTIME.json")
	f = open("players.json") #file should always be "players.json" or something
	for each player in players:
		f.write("START_PLAYER")
		f.write(player.get_ID)
		f.write(player.to_dict())
		f.write("END_PLAYER")
	f.close()
	"""
	pass

async def load_players():
	#TODO:
	"""
	Pseudocode:

	f = open_file(players.json) #doesn't have to be json
	for entry in f:
		#entry is the data between start/end player markers
		id = entry[id]
		players[id] = Players.from_dict(entry[info])
	"""

if __name__ == "__main__":
	#req = requests.get("https://discordapp.com/api/v8/gateway")
	#print(req.headers)
	client.run(os.getenv("DISCORD_BOT_TOKEN"))
	print("Exiting")
