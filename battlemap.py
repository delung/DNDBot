import discord
import re
from responds import Responds
from saveable import Saveable
from abc import ABC, abstractmethod
import asyncio
from node import Node
from typing import Iterable

class Battlemap(Responds):

    GRID_UNIT_LENGTH = 3
    GRID_UNIT_HEIGHT = 1
    ALLOW_DIAGONAL_MOVEMENT = True
    SYMBOL_LEGEND = "W: wall\nD: door\nX: impassable terrain\n?: curio"
    def __init__(self, rows:int, cols:int) -> None:
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise ValueError("Rows and cols must both be integers")
        self.nodes = [[Node(i, j) for j in range(cols)] for i in range(rows)]
        self.rows = rows
        self.cols = cols
        self.legend = dict()
        self.keys = [str(i) for i in range(10)] + [
            "a","b","c","d","e","f","g","h","i","j","k","l","m",
            "n","o","p","q","r","s","t","u","v","w","x","y","z",
        ]
        self.num_chars = 0

    async def get_response(self, message: discord.Message) -> discord.Embed:
        get_map = re.compile(r"\$mapshow")
        add_wall = re.compile(r"\$mapadd wall [0-9]+,[0-9]+($| [0-9]*,[0-9]*$)")
        add_imp = re.compile(r"\$mapadd impassable [0-9]+,[0-9]+($| [0-9]*,[0-9]*$)")
        add_door = re.compile(r"\$mapadd door [0-9]+,[0-9]+$")
        add_curio = re.compile(r"\$mapadd curio [0-9]+,[0-9]+$")
        add_char = re.compile(r"\$mapadd char [a-zA-Z]+ [0-9]+,[0-9]+$")
        move_char = re.compile(r"\$mapmove [0-9] [0-9]+,[0-9]+ [0-9]+$")
        remove_obj = re.compile(r"\$maprem [0-9]+,[0-9]+$")
        remove_all = re.compile(r"\$maprem all$")
        help = re.compile(r"\$map help$")

        #for anything involving the node grid, check that coords are in bounds
        #check that requested map size is reasonable
        if not help.match(message.content) is None:
            return await self.get_help_message(message)
        elif not get_map.match(message.content) is None:
            return await self.get_grid()
        elif not add_char.match(message.content) is None:
            x, y = re.findall(r"[0-9]+", message.content[12:])
            x, y = int(x), int(y)
            valid, msg = await self.__is_valid(x, y)
            if not valid:
                return msg
            name = re.findall(r"[a-zA-Z]+", message.content[12:])[0]
            return await self.add_char((x, y), name)
        elif not add_wall.match(message.content) is None:
            nums = re.findall(r"[0-9]+", message.content[12:])
            if len(nums) == 4:
                x, y, a, b = nums
                x, y, a, b = int(x), int(y), int(a), int(b)
                valid, msg, _ = await self.__is_path_valid((x, y), (a, b))
                if not valid:
                    return msg
                return await self.add_wall((x, y), (a, b))
            else:
                x, y = nums
                x, y = int(x), int(y)
                valid, msg = await self.__is_valid(x, y)
                if not valid:
                    return msg
                return await self.add_wall((int(x), int(y)))
        elif not move_char.match(message.content) is None:
            key = re.findall(r" ([a-z]|[0-9]) ", message.content[8:])[0]
            mvmnt = re.findall(r"[0-9]+$", message.content[8:])[0]
            coord_match = re.findall(r"[0-9]+,[0-9]+", message.content[8:])
            x, y = coord_match[0].split(",")
            x, y, mvmnt = int(x), int(y), int(mvmnt)
            char_name, curr_loc = self.legend[key]
            await self.remove_obj(curr_loc)
            valid, msg, path = await self.__is_path_valid(curr_loc, (x, y))
            if not valid:
                await self.add_char(curr_loc, char_name)
                return msg
            max_possible_steps = mvmnt // 5
            max_mvmnt_path = path[1:1+max_possible_steps]
            final_loc = max_mvmnt_path[len(max_mvmnt_path)-1]
            return await self.add_char(final_loc, char_name)
        elif not add_imp.match(message.content) is None:
            nums = re.findall(r"[0-9]+", message.content[17:])
            if len(nums) == 4:
                x, y, a, b = nums
                x, y, a, b = int(x), int(y), int(a), int(b)
                valid, msg, _ = await self.__is_path_valid((x, y), (a, b))
                if not valid:
                    return msg
                return await self.add_impassable((x, y), (a, b))
            else:
                x, y = nums
                x, y = int(x), int(y)
                valid, msg = await self.__is_valid(x, y)
                if not valid:
                    return msg
                return await self.add_impassable((int(x), int(y)))
        elif not add_door.match(message.content) is None:
            nums = re.findall(r"[0-9]+", message.content[12:])
            x, y = nums
            x, y = int(x), int(y)
            valid, msg = await self.__is_valid(x, y)
            if not valid:
                return msg
            return await self.add_door((int(x), int(y)))
        elif not add_curio.match(message.content) is None:
            nums = re.findall(r"[0-9]+", message.content[13:])
            x, y = nums
            x, y = int(x), int(y)
            valid, msg = await self.__is_valid(x, y)
            if not valid:
                return msg
            return await self.add_curio((int(x), int(y)))
        elif not remove_obj.match(message.content) is None:
            nums = re.findall(r"[0-9]+", message.content[7:])
            x, y = nums
            x, y = int(x), int(y)
            return await self.remove_obj((int(x), int(y)))
        elif not remove_all.match(message.content) is None:
            return await self.remove_all()
        else:
            return await self.get_usage_message(message)


    @staticmethod
    async def get_help_message(message: discord.Message) -> discord.Embed:
        emb = discord.Embed()
        emb.title = "Map Help"
        emb.description = "this will eventually tell you how to use the map"
        return emb

    @staticmethod
    async def get_usage_message(message: discord.Message) -> discord.Embed:
        emb = discord.Embed()
        emb.title = "Map Usage"
        emb.description = "this will eventually tell you how to use the map"
        return emb

    @staticmethod
    async def __arange(count: int) -> Iterable:
        for i in range(count):
            yield(i)

    async def __is_valid(self, x: int, y: int) -> (bool, discord.Embed):
        if x < 0 or x >= self.rows or y >= self.cols or y < 0:
            emb = discord.Embed()
            emb.title = "Location " + str(x) + "," + str(y) + " is out of bounds."
            return False, emb
        if self.nodes[x][y].impassable:
            emb = discord.Embed()
            emb.title = "Location " + str(x) + "," + str(y) + " is occupied or not passable."
            return False, emb
        return True, None

    async def __is_path_valid(self, start_loc: tuple, end_loc: tuple) -> tuple:
        path = await self.find_path(start_loc, end_loc)
        if path is None:
            emb = discord.Embed()
            emb.title = "Path from " + str(start_loc) + " to " + str(end_loc) + \
                "impossible. Something is either there, or coords are invalid."
            return False, emb, None
        for x, y in path:
            valid, msg = await self.__is_valid(x, y)
            if not valid:
                emb = discord.Embed()
                emb.title = "Path impossible. " + \
                    "Location " + str(x) + "," + str(y) + " is invalid."
                return False, emb, None
        return True, None, path

    async def add_door(self, loc: tuple) -> discord.Embed:
        await self.nodes[loc[0]][loc[1]].set_door()
        return await self.get_grid()

    async def add_wall(self, start_loc: tuple, end_loc: tuple=None) -> discord.Embed:
        if not end_loc is None:
            path = await self.find_path(start_loc, end_loc)
            for row, col in path:
                await self.nodes[row][col].set_wall()
        else:
            await self.nodes[start_loc[0]][start_loc[1]].set_wall()
        return await self.get_grid()

    async def add_char(self, loc: tuple, name: str) -> discord.Embed:
        #Needs to keep track of legend and which symbol to use
        if self.num_chars == 36:
            raise SystemError("Too many characters on battle grid, can't add")
        self.num_chars += 1
        k = str(self.keys.pop(0))
        self.legend[k] = [name, (loc[0], loc[1])]
        await self.nodes[loc[0]][loc[1]].set_char(k)
        return await self.get_grid()

    async def add_impassable(self, start_loc: tuple, end_loc: tuple=None) -> discord.Embed:
        if not end_loc is None:
            path = await self.find_path(start_loc, end_loc)
            for row, col in path:
                await self.nodes[row][col].set_impassable()
        else:
            await self.nodes[start_loc[0]][start_loc[1]].set_impassable()
        return await self.get_grid()

    async def add_curio(self, loc: tuple) -> discord.Embed:
        await self.nodes[loc[0]][loc[1]].set_curio()
        return await self.get_grid()

    async def remove_obj(self, start_loc: tuple, end_loc: tuple=None) -> discord.Embed:
        if not end_loc is None:
            path = await self.find_path(start_loc, end_loc, True)
            for coord in path:
                if self.nodes[coord[0]][coord[1]].is_char:
                    k = self.nodes[coord[0]][coord[1]].symbol
                    self.keys += [k]
                    self.legend[k] = None
                await self.nodes[coord[0]][coord[1]].set_empty()
        else:
            if self.nodes[start_loc[0]][start_loc[1]].is_char:
                k = self.nodes[start_loc[0]][start_loc[1]].symbol
                self.keys += [k]
                self.legend[k] = None
            await self.nodes[start_loc[0]][start_loc[1]].set_empty()
        self.keys.sort()
        return await self.get_grid()

    async def remove_all(self) -> discord.Embed:
        for i in range(self.rows):
            for j in range(self.cols):
                if self.nodes[i][j].is_char:
                    k = self.nodes[i][j].symbol
                    self.keys += [k]
                    self.legend[k] = None
                await self.nodes[i][j].set_empty()
        self.keys.sort()
        return await self.get_grid()

    async def get_legend(self) -> str:
        to_be_printed = ""
        for k, v in self.legend.items():
            if not v is None:
                to_be_printed += k + ") " + v[0] + "\n"
        return to_be_printed

    async def get_grid(self) -> discord.Embed:
        if self.GRID_UNIT_LENGTH % 2 != 1:
            raise ValueError("Battlemap Grid unit length must be an odd number.")
        if self.GRID_UNIT_LENGTH <= 1:
            raise ValueError("Battlemap Grid unit length must be > 1")
        if self.GRID_UNIT_HEIGHT < 1:
            raise ValueError("Battlemap Grid unit height must be > 0")
        if self.GRID_UNIT_LENGTH % 2 != 1:
            raise ValueError("Battlemap Grid unit height must be an odd number.")

        horz_div = "+" + ("-" * self.GRID_UNIT_LENGTH)
        vert_div = "|" + (" " * self.GRID_UNIT_LENGTH)
        to_be_printed = [" " + (" " * (self.GRID_UNIT_LENGTH//2)) + \
            str(i) + (" " * (self.GRID_UNIT_LENGTH//2)) \
            for i in range(self.cols)]
        to_be_printed = " " + "".join(to_be_printed) + "\n"
        temp_str = ""
        async for i in Battlemap.__arange(self.rows):
            to_be_printed += " " + horz_div * self.cols + "+\n"
            async for l in Battlemap.__arange(self.GRID_UNIT_HEIGHT):
                if l == self.GRID_UNIT_HEIGHT//2:
                    temp_str = str(i)
                else:
                    temp_str = " "
                async for j in Battlemap.__arange(self.cols):
                    temp_str += "|"
                    async for k in Battlemap.__arange(self.GRID_UNIT_LENGTH):
                        if l == self.GRID_UNIT_HEIGHT//2 and \
                        k == self.GRID_UNIT_LENGTH//2:
                            temp_str += self.nodes[i][j].symbol
                        else:
                            temp_str += " "
                to_be_printed += temp_str + "|\n"
        to_be_printed += " " + horz_div * self.cols + "+\n"
        to_be_printed = "```" + to_be_printed + "```"
        legend = await self.get_legend()

        emb = discord.Embed()
        emb.title = ""
        emb.type = "rich"
        emb.add_field(name="Map", value=to_be_printed, inline=False)
        #emb.add_field(name="\u200b", value="\u200b", inline=True)
        emb.add_field(name="Symbols", value=self.SYMBOL_LEGEND, inline=True)
        if legend != "" and not legend is None:
            emb.add_field(name="Legend", value=legend, inline=True)
        emb.colour = discord.Colour.dark_red()
        return emb

    async def initialize_nodes(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                await self.nodes[row][col].initialize()

    async def find_path(self, start_coord: tuple, end_coord: tuple, ignore_impassable: bool=False) -> list:
        await self.initialize_nodes()
        q = asyncio.PriorityQueue()
        start = self.nodes[start_coord[0]][start_coord[1]]
        dest = self.nodes[end_coord[0]][end_coord[1]]
        nodes_to_ignore = [start]
        iters = 0
        if self.ALLOW_DIAGONAL_MOVEMENT:
            neighbors = [
                (-1, 0), (1, 0), (0, 1), (0, -1),
                (-1, 1), (-1, -1), (1, 1), (1, -1)
            ]
        else:
            neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        await q.put((0, start))
        start.prev_dist = 0

        curr = None
        while not q.empty():
            #get returns a tuple of (priority, data)
            curr = (await q.get())[1]
            if curr == dest:
                break
            if iters >= 100:
                raise SystemError("Max iterations in pathfinding exceeded.")

            for row_mod, col_mod in neighbors:
                #Check that the neighbor is valid and in-bounds
                if curr.col + col_mod < 0 or curr.col + col_mod >= self.cols:
                    continue
                if curr.row + row_mod < 0 or curr.row + row_mod >= self.rows:
                    continue
                #grab the first valid neigbor node
                temp = self.nodes[curr.row+row_mod][curr.col+col_mod]
                if temp.impassable and not ignore_impassable:
                    nodes_to_ignore += [temp]
                    continue
                if temp in nodes_to_ignore:
                    continue
                #priority before = estimated dist + distance from prev. node
                prior_before_update = await temp.get_priority(dest)
                """
                Actual prior. = est. dist + dist from curr + edge weight
                between curr and temp. Edge weights should all be 1, but I set
                diagonal edges to be 1.7 distance to prioritze horz/vert
                """
                diag = 1.7 if (row_mod != 0 and col_mod != 0) else 1
                prior_after_update = curr.prev_dist + diag + \
                    (await temp.heuristic(dest))

                if prior_after_update < prior_before_update and temp != curr:
                    temp.prev_dist = curr.prev_dist + diag
                    temp.parent = curr
                    await q.put((await temp.get_priority(dest), temp))
            iters += 1

        if curr == dest:
            path = []
            while not curr.parent is None:
                path += [(curr.row, curr.col)]
                curr = curr.parent
            return [(start.row, start.col)] + path[::-1]
        else:
            return None
