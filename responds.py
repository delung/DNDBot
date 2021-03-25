from abc import ABC, abstractmethod
import discord
import asyncio

class Responds(ABC):

	@abstractmethod
	async def get_response(message: discord.Message) -> discord.Embed:
		pass
	
	@abstractmethod
	async def get_help_message(message: discord.Message) -> discord.Embed:
		pass
	
	@abstractmethod
	async def get_usage_message(message: discord.Message) -> discord.Embed:
		pass