import asyncio
from websockets import server
from compute_actions import compute, MemoizationStruct
import random
from game_adapter import json_of_game_state

from projectl import ProjectLGame


async def handler(websocket: server.WebSocketServerProtocol):
    game = ProjectLGame(2)
    mem = MemoizationStruct.new()
    while True:
        await websocket.send(json_of_game_state(game.extract_state()))
        possible_actions = compute(game, mem)
        if len(possible_actions) == 0:
            return
        (random_action, _) = random.choice(possible_actions)
        game.step(random_action)


async def main():
    async with server.serve(handler, "localhost", 8765):
        print("started server on ws://localhost:8765")
        await asyncio.Future()  # run forever


asyncio.run(main())
