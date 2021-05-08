import discord
import re

async def new_sheet(message: discord.Message) -> discord.Embed:
    emb = discord.Embed()
    emb.title = '$player update_sheet\nCharacter Sheet'
    emb.description = 'WIP - does nothing right now'

    details = 'CHARACTER NAME = []\n Class = []\nLevel = []\nRace = []\nPROFICIENCY BONUS = []\n'

    ability_score = 'STRENGTH = [][]\nDEXTERITY = [][]\nCONSTITUTION = [][]\n' + \
    'INTELLIGENCE = [][]\nWISDOM = [][]\nCHARISMA = [][]\n'
    saving_throws = 'STRENGTH = [][]\nDEXTERITY = [][]\nCONSTITUTION = [][]\n' + \
    'INTELLIGENCE = [][]\nWISDOM = [][]\nCHARISMA = [][]\n'

    skills = 'Acrobatics (Dex) = [][]\nAnimal Handling (Wis) = [][]\n' + \
    'Arcana (Int) = [][]\n Athletics (Str) = [][]\nDeception (Cha) = [][]\n' + \
    'History (Int) = [][]\nInsight (Wis) = [][]\nIntimidation (Cha) = [][]\n' + \
    'Investigation (Int) = [][]\nMedicine (Wis) = [][]\nNature (Int) = [][]\n' + \
    'Perception (Wis) = [][]\nPerformance (Cha) = [][]\nPersuasion (Cha) = [][]\n' + \
    'Religion (Int) = [][]\nSleight of Hand (Dex) = [][]\nStealth (Dex) = [][]\n' + \
    'Survival (Wis) = [][]\n'

    stats = 'ARMOR CLASS = []\nSPEED = []\nHIT POINT MAXIMUM = []\n'


    emb.add_field(name='Character Details:', value = details, inline=False)
    emb.add_field(name='Ability Score (Ex. [raw score][modifier] -> [13][+2]):', value = ability_score, inline=False)
    emb.add_field(name='Saving Throws (Ex. [!][+7] use ! in the first box to denote skill proficiency):', value = saving_throws, inline=False)
    emb.add_field(name='Skills (Ex. [!][+7] use ! in the first box to denote skill proficiency):', value = skills, inline=False)
    emb.add_field(name='Stats:', value = stats, inline=False)
    return emb


async def sample_sheet(message: discord.Message) -> discord.Embed:
    emb = discord.Embed()
    emb.title = 'Sample Character Sheet'
    emb.description = 'Sample Sheet'

    details = 'CHARACTER NAME = [Hero]\n Class = [Figther]\nLevel = [1]\nRace = [Human]\nPROFICIENCY BONUS = [+2]\n'

    ability_score = 'STRENGTH = [20][+5]\nDEXTERITY = [20][+5]\nCONSTITUTION = [20][+5]\n' + \
    'INTELLIGENCE = [20][+5]\nWISDOM = [20][+5]\nCHARISMA = [20][+5]\n'
    saving_throws = 'STRENGTH = [!][+7]\nDEXTERITY = [!][+7]\nCONSTITUTION = [][+5]\n' + \
    'INTELLIGENCE = [][+5]\nWISDOM = [][+5]\nCHARISMA = [][+5]\n'

    skills = 'Acrobatics (Dex) = [!][+7]\nAnimal Handling (Wis) = [][+5]\n' + \
    'Arcana (Int) = [!][+7]\n Athletics (Str)\nDeception (Cha) = [][+5]\n' + \
    'History (Int) = [][+5]\nInsight (Wis) = [][+5]\nIntimidation (Cha) = [][+5]\n' + \
    'Investigation (Int) = [][+5]\nMedicine (Wis) = [][+5]\nNature (Int) = [][+5]\n' + \
    'Perception (Wis) = [][+5]\nPerformance (Cha) = [][+5]\nPersuasion (Cha) = [][+5]\n' + \
    'Religion (Int) = [][+5]\nSleight of Hand (Dex) = [!][+7]\nStealth (Dex) = [][+5]\n' + \
    'Survival (Wis) = [][+5]\n'

    stats = 'ARMOR CLASS = [20]\nSPEED = [30]\nHIT POINT MAXIMUM = [50]\n'


    emb.add_field(name='Character Details:', value = details, inline=False)
    emb.add_field(name='Ability Score (Ex. [!][+7] use ! in the first box to denote skill proficiency):', value = ability_score, inline=False)
    emb.add_field(name='Saving Throws:', value = saving_throws, inline=False)
    emb.add_field(name='Skills (Ex. [!][+7] use ! in the first box to denote skill proficiency):', value = skills, inline=False)
    emb.add_field(name='Stats:', value = stats, inline=False)
    return emb

async def sheet_accepted(message: discord.Message) -> discord.Embed:
    emb = discord.Embed()
    emb.title = 'Sheet Accepted'
    return emb
