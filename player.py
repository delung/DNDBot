import discord
import re
from responds import Responds
from abc import ABC, abstractmethod
import asyncio

class Player(Responds):
    """
    1. Player types $new character
    2. main.py will call the get_new_char_form() function from player
    3. Upon recieving a DM of the filled out form, instantiates a new player
    by extracting the info from the DM'ed message
    """

    def __init__(self: Player, discord_id: str,
            ch: Character(), health: int, inv: Inventory) -> None:
        """
        Constructor
        """
        self.discord_id = discord_id #discord user ID
        self.character = ch #Add arguments
        self.health = health #Start at 1 maybe, gets updated with $set health
        self.inv = inv
        pass

    @classmethod
    async def from_dict(d: dict) -> Player:
        """
        extracts info from d
        """
        #discord_id = d[id]
        #health = health[id]
        #character = Character.from_dict(d[character])
        #inv = Inventory.from_dict(d[inv])
        #return player(discord_id, health, charcter)
        pass

    @classmethod
    async def to_dict(self: Player) -> dict:
        """
        Returns a dictionary with all relevant fields and attributes.
        """
        #d[id] = self.discord_id
        #d[health] = self.health
        #d[character] = self.character.to_dict()
        #d[inv] = self.inv.to_dict()
        pass

    async def add_item(self: Player, item_name: str) -> discord.Embed:
        """
        Interact with self.inv however necessary
        Generate embed messsage with "item_name" added to inv. and return it
        """
        pass

    async def set_ac(self: Player, ac: int) -> discord.Embed:
        """
        Interact with self.ac however necessary
        Generate embed messsage with "ac set to" + str(self.ac). and return it
        """
        pass

    @staticmethod
    async def get_response(message: discord.Message) -> discord.Embed:
        """
        regexs the message from main.py to determine if they are:
        1. Making a new character ($new character)
        2. Setting some stat ($set health 30)
        3. Messing with inventory ($add item pingas)
        4. Trading ($send item pingas MuhWashington
        or $send money 10 MuhWashington) Money will be stored as copper
        5. Asking for help ($character help)
        6. A secret dm function ($dmsend money 300 MuhWashington)
        7. Another secret dm function ($dmadd item peepee MuhWashington)

        Calls the appropriate function and returns an embed message with the
        response based on what happened.

        For 1. specifically, it will DM the user that asked.
        For 6. and 7., it should also check the role of sender to make sure
        they can use the secret DM functions.

        Optionally, when something is added/taken away, DM who is affected.

        Set/get health can just be done in here. If $get health then return
        an embed message with @user, current health is + str(self.health)

        add_item will call self.add_item, which returns a message to send to
        user
        """
        pass

    @staticmethod
    async def get_help_message(message: discord.Message) -> discord.Embed:
        pass

    @staticmethod
    async def get_usage_message(message: discord.Message) -> discord.Embed:
		pass

    @staticmethod
    async def get_new_char_form() -> discord.Message:
        """

        """
        pass
