#Static class for rolling support
import asyncio
import re
import random

class Rolling:

  MAX_ROLLS = 1000
  MAX_ROLLS_TO_SHOW_INDIVIDUAL_ROLLS = 20

  @staticmethod
  async def __print_usage_message(msg):
    """
    When incorrect usage of the roll command is done, this @s the user and tells them how to
    get help
    """
    print("This is not done yet")
    await msg.channel.send(msg.author.mention + " You messed up, but I can't help you yet")
    return

  @staticmethod
  async def __print_help(msg):
    """
    private helper class that prints how to use the roll command when a mistake is made
    """
    print("help is not coming")
    await msg.channel.send(msg.author.mention + " Help is not coming.")
    return
  
  @staticmethod
  async def __print_formatted_rolls(rolls, roll_total, msg):
    """
    Takes the rolls 
    rolls: list of ints corresponding to the numbers rolled
    roll_total: sum of all rolls in rolls
    msg: original message to obtain channel/username info to @ them in reply
    """
    if (len(rolls) == 1):
      await msg.channel.send(msg.author.mention + " you rolled a " + str(roll_total))
    elif (len(rolls) > Rolling.MAX_ROLLS_TO_SHOW_INDIVIDUAL_ROLLS):
      await msg.channel.send(msg.author.mention + " you rolled a total of " + str(roll_total))
    else:
      await msg.channel.send(msg.author.mention + " rolls made: " + str(rolls) + "\n" \
      " you rolled a total of " + str(roll_total))
    return

  @staticmethod
  async def __parse_message(msg):
    """
    Private helper function to parse message and extract info to make rolls
    Doc goes here
    """
    cmd = msg.content
    # split string into numerics and split by continuous number
    int_cmd = re.findall('[0-9]+', cmd[2:])
    str_cmd = re.findall('[a-z]+', cmd[2:])


    """
    The following conditions must be met, or the help will be printed and nothing will ocurr
    1. the character following $r must be a number
    2. the text portion of the command following $r must be length 1
    3. the text portion of the command following $r must be == "d"
    4. there must be 2 numbers in the string following $r, separated by a d
    5. num rolls must be < MAX_ROLLS
    """
    possible_errors = [
      not cmd[2].isnumeric(),
      len(str_cmd) != 1,
      str_cmd[0] != 'd',
      len(int_cmd) != 2,
      int(int_cmd[0]) > Rolling.MAX_ROLLS
    ]

    if any(possible_errors):
      return None

    return int(int_cmd[0]), int(int_cmd[1])

  @staticmethod
  async def __gen_random_num(num_sides):
    return random.randint(1,num_sides)

  @staticmethod
  async def make_roll(msg):
    """
    Doc goes here
    """
    res = await Rolling.__parse_message(msg)
    if (res is None):
      await Rolling.__print_usage_message(msg)
      return

    #Launch num_rolls tasks to generate a random number between 1 and num_sides
    #Gather results into a list called "rolls"
    num_rolls, num_sides = res[0], res[1]
    rolls = await asyncio.gather(*(Rolling.__gen_random_num(num_sides) for n in range(num_rolls)))
    roll_total = sum(rolls)
    await Rolling.__print_formatted_rolls(rolls, roll_total, msg)
    return

  