import discord
import re
from abc import ABC, abstractmethod
import asyncio

class Character:
    def __init__(self: Character, str:int, dex:int, level:int) -> Character:
        self.str = str
        self.dex = dex
        self.level = level
        pass

    @classmethod
    async def from_dict(d: dict) -> Character:
        pass

    @classmethod
    async def to_dict(self: Character) -> dict:
        pass

    async def get_stats(self: Character):
        pass

    async def get_modifiers(self: Character):
        pass

    async def get_skills(self: Character):
        pass

    async def get_level(self: Character):
        pass

    async def set_level(self: Character):
        pass
