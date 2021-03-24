import discord
import os
import asyncio
import re
import requests
from rolling import Rolling
#from keep_alive import keep_alive
#from database import *
from get_gif import *

client = discord.Client()

#Usage message for dice roll
async def help(message):
  await message.channel.send('Ex: $r1d20')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  #Specific regex match for rolls
  roll_regex = re.compile(r"\$r[1-9][0-9]*d[1-9][0-9]*$")

  if message.author == client.user:
    return
  #Message matched roll regex
  elif not roll_regex.match(message.content) is None: 
    await Rolling.make_roll(message)
  elif message.content == '$hello':
    await message.channel.send('https://tenor.com/view/howdy-cowboy-woody-toy-story-shark-gif-5543642')
  elif message.content == '$help':
    await message.channel.send('Eventually this will have a help menu')
  elif message.content == '$REE':
    await message.channel.send(get_ree_gif())
  elif message.content == '$ricardo':
    await message.channel.send(get_ricardo_gif())
  


#db example
#set_value(1,20)
#print(get_value(1))

'''
if __name__ == "__main__":
    #keep_alive()
    req = requests.get("https://discord.com/api/v8/gateway")
    print(req.headers)
    print(req.json())
    #print(req.json())
    #client.run(os.getenv('TOKEN'))
    print("Exiting")

'''