#request format

#user pings bot for form
#bot checks if user already has a sheet
#if not send new form else load old form
#bot dm user form
#parse form to create player/char
#save it
import discord
from responds import Responds

class Char_sheet(Responds):

    async def get_response(message: discord.Message) -> discord.Embed:
        emb = discord.Embed()
        emb.title = 'Character Sheet'

        details = 'CHARACTER NAME = []\n Class = []\nLevel = []\nRace =[]\n'

        ability_score = 'STRENGTH = []\nDEXTERITY = []\nCONSTITUTION = []\n' + \
        'INTELLIGENCE = []\nWISDOM = []\nCHARISMA = []\n'

        skills = 'Acrobatics (Dex) = []\nAnimal Handling (Wis) = []\n' + \
        'Arcana (Int) = []\n Athletics (Str)\nDeception (Cha) = []\n' + \
        'History (Int) = []\nInsight (Wis) = []\nIntimidation (Cha) = []\n' + \
        'Investigation (Int) = []\nMedicine (Wis) = []\nNature (Int) = []\n' + \
        'Perception (Wis) = []\nPerformance (Cha) = []\nPersuasion (Cha) = []\n' + \
        'Religion (Int) = []\nSleight of Hand (Dex) = []\nStealth (Dex) = []\n' + \
        'Survival (Wis) = []\n'

        stats = 'ARMOR CLASS = []\nSPEED = []\nHIT POINT MAXIMUM = []\n'


        emb.add_field(name='Character Details:', value = details, inline=False)
        emb.add_field(name='Ability Score:', value = ability_score, inline=False)
        emb.add_field(name='Saving Throws:', value = ability_score, inline=False)
        emb.add_field(name='Skills:', value = skills, inline=False)
        emb.add_field(name='Stats:', value = stats, inline=False)

        return emb
