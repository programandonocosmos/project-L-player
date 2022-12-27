import asyncio
from websockets import server
from compute_actions import compute
import random
from game_adapter import json_of_game_state

from projectl import ProjectLGame


async def handler(websocket: server.WebSocketServerProtocol):
    game = ProjectLGame(2)
    while True:
        await websocket.send(json_of_game_state(game.extract_state()))
        (random_action, _) = random.choice(compute(game))
        game.step(random_action)


async def main():
    async with server.serve(handler, "localhost", 8765):
        print("started server on ws://localhost:8765")
        print("creating game...")
        await asyncio.Future()  # run forever


asyncio.run(main())
