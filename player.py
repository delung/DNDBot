import discord
import re
from responds import Responds
from saveable import Saveable
from character import Character
from inventory import Inventory
from abc import ABC, abstractmethod
from form import *
import asyncio

class Player(Responds, Saveable):
    """
    1. Player types $new character
    2. main.py will call the get_new_char_form() function from player
    3. Upon recieving a DM of the filled out form, instantiates a new player
    by extracting the info from the DM'ed message
    """

    # this doesnt compile fix it nick

    def __init__(self, discord_id: str, ch: Character, health: int, inv: Inventory) -> None:

        self.discord_id = discord_id #discord user ID
        self.character = ch #Add arguments
        self.health = health #Start at 1 maybe, gets updated with $set health
        self.inv = inv

    @classmethod
    async def from_dict(d: dict):
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
    async def to_dict(self) -> dict:
        """
        Returns a dictionary with all relevant fields and attributes.
        """
        #d[id] = self.discord_id
        #d[health] = self.health
        #d[character] = self.character.to_dict()
        #d[inv] = self.inv.to_dict()
        pass

    async def add_item(self, item_name: str) -> discord.Embed:
        """
        Interact with self.inv however necessary
        Generate embed messsage with "item_name" added to inv. and return it
        """
        pass

    async def set_ac(self, ac: int) -> discord.Embed:
        """
        Interact with self.ac however necessary
        Generate embed messsage with "ac set to" + str(self.ac). and return it
        """
        pass

    @staticmethod
    async def get_response(message: discord.Message) -> discord.Embed:
        """
        regexs the message from main.py to determine if they are:
        1. Making a new character ($player new)
        2. Setting some stat ($player set health 30)
        3. Messing with inventory ($player add item pingas)
        4. Trading ($player send item pingas MuhWashington
        or $player send money 10 MuhWashington) Money will be stored as copper
        5. Asking for help ($player help)
        6. A secret dm function ($dm send money 300 MuhWashington)
        7. Another secret dm function ($dm add item peepee MuhWashington)

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

        # 1 Making a new character $player new
        example_pattern = re.compile(r"\$player new example$")
        new_pattern = re.compile(r"\$player new$")
        update_sheet_pattern = re.compile(r"\$player update_sheet")

        example_match = example_pattern.match(message.content)
        new_match = new_pattern.match(message.content)
        update_sheet_match = update_sheet_pattern.match(message.content)

        print(update_sheet_match)
        if not example_match is None:
            return await sample_sheet(message)

        elif not update_sheet_match is None:
            print("Parsing")
            return await sheet_accepted(message)
        return await new_sheet(message)

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
