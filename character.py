import discord
import re
from saveable import Saveable
from abc import ABC, abstractmethod
import asyncio

class Character():
    def __init__(self, str:int, dex:int, level:int) -> None:
        self.str = str
        self.dex = dex
        self.level = level

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
