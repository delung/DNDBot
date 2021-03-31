import discord
import re
import random
from responds import Responds
from abc import ABC, abstractmethod
import asyncio

class Rolling(Responds):

	MAX_ROLLS = 1000
	MAX_ROLLS_TO_SHOW_INDIVIDUAL_ROLLS = 20

	async def get_response(message: discord.Message) -> discord.Embed:
		roll_pattern = re.compile(r"\$r[1-9][0-9]*d[1-9][0-9]*$")
		help_pattern = re.compile(r"\$r help$")

		roll_match = roll_pattern.match(message.content)
		help_match = help_pattern.match(message.content)

		if not help_match is None:
			return await Rolling.get_help_message(message)
		elif not roll_match is None:
			matches = re.findall('[0-9]+', message.content[2:])
			num_rolls, num_sides = int(matches[0]), int(matches[1])

			if num_rolls == 0 or num_sides == 0:
				return await Rolling.get_usage_message(message)
			elif num_rolls > Rolling.MAX_ROLLS:
				return await Rolling.get_usage_message(message)

			roll_total, rolls = await Rolling.roll(num_rolls, num_sides)
			return await Rolling.__roll_to_response(message, roll_total, rolls,
													num_rolls, num_sides)
		else:
			return await Rolling.get_usage_message(message)

		return await Rolling.get_usage_message(message)

	async def get_help_message(message: discord.Message) -> discord.Embed:
		emb = discord.Embed()
		emb.title = "Help Requested by " + str(message.author.display_name)
		emb.type = "rich"
		emb.add_field(name="Basic Usage", value="Command syntax is \n" + \
			"```$rXdY``` \n " + \
			"Rolls a Y sided die X times.", inline=False)
		emb.add_field(name="Bot Reply", value="The bot will reply to you " + \
			"with a formatted message containing your " + \
			"request, a list of each roll made and the total of the " + \
			"rolls. ***Note that if you roll more than 50 dice, then only " + \
			"the total will be shown to avoid clutter.***", inline=False)
		emb.add_field(name="Max Rolls",
			value="There is currently a ***maximum " + \
			"number of rolls*** (" + str(Rolling.MAX_ROLLS) + ") that " + \
			"can be made in one command before you will be sent usage " + \
			"instructions", inline=False)
		emb.colour = discord.Colour.dark_red()
		return emb

	async def get_usage_message(message: discord.Message) -> discord.Embed:
		emb = discord.Embed()
		emb.title = "How To Use the Roll Command"
		emb.type = "rich"
		emb.description = message.author.mention + "\n" + \
		 "Rolling is `$rXdY` where X is the number of dice and " + \
		 " Y is the number of sides.\n" + \
		 "For help on using roll properly, type `$r help`"
		emb.add_field(name=u'\u200b',
			value="Please note that the max number of rolls is " + \
			str(Rolling.MAX_ROLLS), inline=False)
		emb.colour = discord.Colour.dark_red()
		return emb

	@staticmethod
	async def __gen_random_num(num_sides: int) -> int:
		return random.randint(1,num_sides)

	@staticmethod
	async def roll(num_rolls: int, num_sides: int) -> (int, list):
		"""
		Rolls num_rolls numbers between 1 and num_sides.
		Returns the sum of all rolls, and a list of all rolls made
		"""

		rolls = await asyncio.gather(*(Rolling.__gen_random_num(num_sides)
										for n in range(num_rolls)))
		return sum(rolls), rolls

	@staticmethod
	async def __roll_to_response(message: discord.Message,
		roll_total: int, rolls: list,
		num_rolls: int, num_sides: int) -> discord.Embed:
		"""
		Gets an embed with roll results
		"""
		emb = discord.Embed()
		plural = "s" if num_rolls > 1 else ""
		emb.title = str(message.author.display_name) + " Rolled " + \
			str(num_rolls) + " d" + str(num_sides) + plural
		emb.type = "rich"
		emb.add_field(name="ROLLS:", value=str(rolls)[1:len(str(rolls))-1],
		 		inline=False)
		emb.add_field(name="ROLL TOTAL:", value=str(roll_total), inline=False)
		emb.colour = discord.Colour.from_rgb(0, 0, 0)
		return emb
