import discord
import re
from abc import ABC, abstractmethod
import asyncio

<<<<<<< HEAD
class Character:
=======
class Character(Saveable):
>>>>>>> 752c0f3a7e6a7535328f31aae66adaed77fbc32d
    def __init__(self: Character, str:int, dex:int, level:int) -> None:
        self.str = str
        self.dex = dex
        self.level = level
        pass

    @classmethod
    async def from_dict(d: dict):
        pass

    @classmethod
    async def to_dict(self) -> dict:
        pass

    async def get_stats(self):
        pass

    async def get_modifiers(self):
        pass

    async def get_skills(self):
        pass

    async def get_level(self):
        pass

    async def set_level(self):
        pass
