import discord
import re
from abc import ABC, abstractmethod
import asyncio

class Inventory():

    def __init__(self) -> None:
        pass

    @classmethod
    async def from_dict(d: dict):
        pass

    @classmethod
    async def to_dict(self) -> dict:
        pass

    async def add_item(self):
        pass

    async def remove_item(self):
        pass
