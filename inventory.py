import discord
import re
from abc import ABC, abstractmethod
import asyncio

class Inventory():

    def __init__(self: Inventory) -> Inventory:
        pass

    @classmethod
    async def from_dict(d: dict) -> Inventory:
        pass

    @classmethod
    async def to_dict(self: Inventory) -> dict:
        pass

    async def add_item(self: Inventory):
        pass

    async def remove_item(self: Inventory):
        pass
