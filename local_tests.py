from battlemap import Battlemap
import asyncio

p = Battlemap(3, 5)
print("hi")
print(asyncio.run(p.add_wall((0, 1), (2, 1))))
print(asyncio.run(p.add_door((1, 1))))
print(asyncio.run(p.find_path((0,0), (0,4))))
print("done")
