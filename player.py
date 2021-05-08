import discord
import re
from responds import Responds
from character import Character
from inventory import Inventory
from abc import ABC, abstractmethod
from form import *
import asyncio
import json

re_char_name = 0
re_char_class = 1
re_char_level = 2
re_char_race = 3
re_char_prof_bonus = 4

# char ability score
re_char_str = 5
re_char_dex = 6
re_char_con = 7
re_char_int = 8
re_char_wis = 9
re_char_cha = 10

# char saving throws
re_char_s_str = 11
re_char_s_dex = 12
re_char_s_con = 13
re_char_s_int = 14
re_char_s_wis = 15
re_char_s_cha = 16

# Skills
re_char_acrobatics = 17
re_char_animal_handling = 18
re_char_arcana = 19
re_char_atheletics = 20
re_char_deception = 21
re_char_history = 22
re_char_insight = 23
re_char_intimidation = 24
re_char_investigation = 25
re_char_medicine = 26
re_char_nature = 27
re_char_perception = 28
re_char_performance = 29
re_char_religion = 30
re_char_sleight_of_hand = 31
re_char_stealth = 32
re_char_survival = 33

re_char_ac = 34
re_char_speed = 35
re_char_max_hit = 36

class Player(Responds):
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
    async def parse_form(message: discord.Message) -> discord.Embed:
        """
        1. create loop starting at first line.
        2. Move to next element until expected regex is found
        3. else return error
        """
        sheet = message.content.splitlines()
        re_list = [None] * 37
        stat_dict = {}
        # char details

        re_list[re_char_name] = re.compile(r"CHARACTER NAME = \[(.*?)\]")
        re_list[re_char_class] = re.compile(r"Class = \[(.*?)\]")
        re_list[re_char_level] = re.compile(r"Level = \[(.*?)\]")
        re_list[re_char_race] = re.compile(r"Race = \[(.*?)\]")
        re_list[re_char_prof_bonus] = re.compile(r"PROFICIENCY BONUS = \[(.*?)\]")

        # char ability score
        re_list[re_char_str] = re.compile(r"STRENGTH = \[(.*)+\]\[(.*)+\]")
        re_list[re_char_dex] = re.compile(r"DEXTERITY = \[(.*)+\]\[(.*)+\]")
        re_list[re_char_con] = re.compile(r"CONSTITUTION = \[(.*)+\]\[(.*)+\]")
        re_list[re_char_int] = re.compile(r"INTELLIGENCE = \[(.*)+\]\[(.*)+\]")
        re_list[re_char_wis] = re.compile(r"WISDOM = \[(.*)+\]\[(.*)+\]")
        re_list[re_char_cha] = re.compile(r"CHARISMA = \[(.*)+\]\[(.*)+\]")

        # char saving throws
        re_list[re_char_s_str] = re.compile(r"STRENGTH = \[(!|)\]\[(.*)+\]")
        re_list[re_char_s_dex] = re.compile(r"DEXTERITY = \[(!|)\]\[(.*)+\]")
        re_list[re_char_s_con] = re.compile(r"CONSTITUTION = \[(!|)\]\[(.*)+\]")
        re_list[re_char_s_int] = re.compile(r"INTELLIGENCE = \[(!|)\]\[(.*)+\]")
        re_list[re_char_s_wis] = re.compile(r"WISDOM = \[(!|)\]\[(.*)+\]")
        re_list[re_char_s_cha] = re.compile(r"CHARISMA = \[(!|)\]\[(.*)+\]")

        # Skills
        re_list[re_char_acrobatics] = re.compile(r"Acrobatics \(Dex\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_animal_handling] = re.compile(r"Animal Handling \(Wis\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_arcana] = re.compile(r"Arcana \(Int\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_atheletics] = re.compile(r"Athletics \(Str\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_deception] = re.compile(r"Deception \(Cha\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_history] = re.compile(r"History \(Int\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_insight] = re.compile(r"Insight \(Wis\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_intimidation] = re.compile(r"Intimidation \(Cha\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_investigation] = re.compile(r"Investigation \(Int\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_medicine] = re.compile(r"Medicine \(Wis\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_nature] = re.compile(r"Nature \(Int\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_perception] = re.compile(r"Perception \(Wis\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_performance] = re.compile(r"Performance \(Cha\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_religion] = re.compile(r"Religion \(Int\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_sleight_of_hand] = re.compile(r"Sleight of Hand \(Dex\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_stealth] = re.compile(r"Stealth \(Dex\) = \[(!|)\]\[(.*)+\]")
        re_list[re_char_survival] = re.compile(r"Survival \(Wis\) = \[(!|)\]\[(.*)+\]")

        re_list[re_char_ac] = re.compile(r"ARMOR CLASS = \[(.*?)\]")
        re_list[re_char_speed] = re.compile(r"SPEED = \[(.*?)\]")
        re_list[re_char_max_hit] = re.compile(r"HIT POINT MAXIMUM = \[(.*?)\]")

        regex_content_1 = re.compile(r"\[(.*?)\]")
        regex_content_2 = re.compile(r"\[(.*?)\]\[(.*?)\]")

        str_index = 0
        regex_index = 0

        while str_index < len(sheet) and regex_index < len(re_list):
            if re_list[regex_index].match(sheet[str_index]):

                if not (regex_match_2 := regex_content_2.search(sheet[str_index])) is None:
                    tuple = (regex_match_2.group(1), regex_match_2.group(2))
                    stat_dict[regex_index] = tuple

                elif not (regex_match_1 := regex_content_1.search(sheet[str_index])) is None:
                    tuple = ('',regex_match_1.group(1))
                    stat_dict[regex_index] = tuple

                regex_index = regex_index + 1

            str_index = str_index + 1

        # end of loop creates dictionary of stats
        print(stat_dict.values())

        emb = discord.Embed()

        print(regex_index)
        print(len(re_list))
        # if something was missing in the form and it isnt exact - send error
        if regex_index != len(re_list):
            emb.description = 'Error - form isnt correct or missing element\n'
        else:
            emb.description = json.dumps(stat_dict)
        return emb

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
            return await Player.parse_form(message)
            #return await sheet_accepted(message)
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
