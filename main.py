import discord
import os
import asyncio
import re
import requests
import pickle
from datetime import datetime
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
	global players
	global bm
	cwd = os.getcwd()
    player_backup = cwd + r"/backups/player_backups/player_backup.bin"
    bm_backup = cwd + r"/backups/bm_backups/bm_backup.bin"
    if os.path.exists(player_backup):
		players = await load_players()
    if os.path.exists(bm_backup):
		bm = await load_bm()
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
	MAX_ROWS_TIMES_COLS = 100
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
	global client
	while not client.is_closed:
		asyncio.sleep(3600) #wait one hour
		saved_players = await save_players_to_file()
		saved_bm = await save_bm_to_file()
		if saved_bm:
			print("saved battlemap successfully")
		if saved_players:
			print("saved battlemap successfully")

		cwd = os.getcwd()
		player_file_prefix = cwd + r"/backups/player_backups/"
		bm_file_prefix = cwd + r"/backups/bm_backups/"
		player_fname = "players_backup"
		bm_fname = "bm_backup"
		file_postfix = ".bin"

		for pre, name in [(player_file_prefix, player_fname + file_postfix), (bm_file_prefix, bm_fname + file_postfix)]:
			if os.path.exists(pre):
				list_of_files = os.listdir(pre)
				if name in list_of_files:
				    list_of_files.remove(name)
				list_of_files = [pre + l for l in list_of_files]
				if len(list_of_files) > 100:
				    oldest_file = min(list_of_files, key=os.path.getctime)
				    print("Removing " + oldest_file)
				    os.remove(os.path.abspath(oldest_file))
	return

async def save_players_to_file() -> bool:
    global players
    cwd = os.getcwd()
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
    file_prefix = cwd + r"/backups/player_backups/"
    file_postfix = ".bin"
    if not os.path.exists(file_prefix):
        os.makedirs(file_prefix)
    fname = r"players_backup"
    frename = r"players_backup_" + date
    iters = 0
    while (True):
        if (os.path.exists(file_prefix + frename + file_postfix)):
            frename += "_new"
        else:
            break
        if iters > 10:
            raise IOError("Too many backups at the same date/time")
        iters += 1
    if (os.path.exists(file_prefix + fname + file_postfix)):
        os.rename(file_prefix + fname + file_postfix, file_prefix + frename + file_postfix)
    file = open(file_prefix + fname + file_postfix, "bw+")
    pickle.dump(players, file)
    file.close()
    return True

async def load_players() -> dict:
    cwd = os.getcwd()
    file_prefix = cwd + r"/backups/player_backups/"
    if not os.path.exists(file_prefix):
        return None
    fname = r"players_backup.bin"
    if (os.path.exists(file_prefix + fname)) and os.path.getsize(file_prefix + fname) > 0:
        file = open(file_prefix + fname, "rb")
        players = pickle.load(file)
        file.close()
        return players
    return None

async def save_bm_to_file() -> bool:
    global bm
    cwd = os.getcwd()
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
    file_prefix = cwd + r"/backups/bm_backups/"
    file_postfix = ".bin"
    if not os.path.exists(file_prefix):
        os.makedirs(file_prefix)
    fname = r"bm_backup"
    frename = r"bm_backup_" + date
    iters = 0
    while (True):
        if (os.path.exists(file_prefix + frename + file_postfix)):
            frename += "_new"
        else:
            break
        if iters > 10:
            raise IOError("Too many backups at the same date/time")
        iters += 1
    if (os.path.exists(file_prefix + fname + file_postfix)):
        os.rename(file_prefix + fname + file_postfix, file_prefix + frename + file_postfix)
    file = open(file_prefix + fname + file_postfix, "bw+")
    pickle.dump(bm, file)
    file.close()
    return True

async def load_bm() -> Battlemap:
    cwd = os.getcwd()
    file_prefix = cwd + r"/backups/bm_backups/"
    if not os.path.exists(file_prefix):
        return None
    fname = r"bm_backup.bin"
    if (os.path.exists(file_prefix + fname)) and os.path.getsize(file_prefix + fname) > 0:
        file = open(file_prefix + fname, "rb")
        bm = pickle.load(file)
        file.close()
        return bm
    return None

if __name__ == "__main__":
	#req = requests.get("https://discordapp.com/api/v8/gateway")
	#print(req.headers)
	client.run(os.getenv("DISCORD_BOT_TOKEN"))
	print("Exiting")
