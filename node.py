from saveable import Saveable
from math import sqrt, inf

class Node(Saveable):

    def __init__(self, row: int, col: int, parent=None) -> None:
        self.symbol = " "
        self.parent = parent
        self.row = row
        self.col = col
        self.prev_dist = inf
        self.impassable = False
        self.is_char = False

    def __repr__(self) -> str:
        rep = ("Loc: (" + str(self.row) + "," + str(self.col) + ")" + \
        " impassable: " + str(self.impassable))
        return rep

    def __lt__(self, other) -> bool:
        return self.row < other.row and self.col < other.col

    def __gt__(self, other) -> bool:
        return self.row > other.row and self.col > other.col

    def __eq__(self, other) -> bool:
        return self.row == other.row and self.col == other.col

    async def initialize(self) -> None:
        self.parent = None
        self.prev_dist = inf
        return

    async def heuristic(self, dest) -> float:
        #Manhattan distance heuristic
        return abs(self.row - dest.row) + abs(self.col - dest.col)

    """
    #Euclidean distance prioritizes diagonals, gives weird solutions
    async def heuristic(self, dest) -> float:
        return sqrt(abs(self.row - dest.row)**2 + abs(self.col - dest.col)**2)
    """

    async def get_priority(self, dest) -> float:
        return (await self.heuristic(dest)) + self.prev_dist

    async def set_empty(self) -> None:
        self.is_char = False
        self.impassable = False
        self.symbol = " "
        return

    async def is_empty(self) -> bool:
        return self.is_char == False and self.symbol == " "

    async def set_impassable(self) -> None:
        self.is_char = False
        self.impassable = True
        self.symbol = "⊗"
        return

    async def set_wall(self) -> None:
        self.is_char = False
        self.impassable = True
        self.symbol = "∎"
        return

    async def set_door(self) -> None:
        self.is_char = False
        self.impassable = False
        self.symbol = "⨅"
        return

    async def set_curio(self) -> None:
        self.is_char = False
        self.impassable = False
        self.symbol = "⁉"
        return

    async def set_char(self, symbol: str) -> None:
        self.is_char = True
        self.impassable = True
        self.symbol = symbol
        return

    async def to_dict(self) -> dict:
        return {"test_key" : "test_val"}

    @staticmethod
    async def from_dict(d: dict):
        return Node()
