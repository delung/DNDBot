from abc import ABC, abstractmethod
import asyncio

class Saveable(ABC):

	@abstractmethod
	async def to_dict(self) -> dict:
		pass

	@abstractmethod
	async def from_dict(d: dict):
		pass
