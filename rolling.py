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
			
			if num_rolls > Rolling.MAX_ROLLS:
				return await Rolling.get_usage_message(message)
				
			roll_total, rolls = await Rolling.roll(num_rolls, num_sides)
			return await Rolling.__roll_to_response(roll_total, rolls)
		else:
			return await Rolling.get_usage_message(message)
		
		return await Rolling.get_usage_message(message)
	
	async def get_help_message(message: discord.Message) -> discord.Embed:
		return discord.Embed(title="temp help response")
	
	async def get_usage_message(message: discord.Message) -> discord.Embed:
		return discord.Embed(title="temp usage response")
	
	@staticmethod
	async def __gen_random_num(num_sides: int) -> int:
		return random.randint(1,num_sides)

	@staticmethod
	async def roll(num_rolls: int, num_sides: int) -> (int, list):
		"""
		Rolls num_rolls numbers between 1 and num_sides.
		Returns the sum of all rolls, and a list of all rolls made
		"""
		
		rolls = await asyncio.gather(*(Rolling.__gen_random_num(num_sides) for n in range(num_rolls)))
		return sum(rolls), rolls
	
	@staticmethod
	async def __roll_to_response(roll_total: int, rolls: list) -> discord.Embed:
		return discord.Embed(title="temp roll response")