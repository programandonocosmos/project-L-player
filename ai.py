from compute_actions import compute
from projectl import ProjectLGame, PuzzleData, VisibleState, ActionData
import torch
import torch.nn as nn
import typing
import os

STATE_VEC_LEN = 459


def puzzle_to_vec(puzzle: typing.Optional[PuzzleData]) -> typing.List[int]:
    if puzzle is None:
        return [0 for _ in range(27)]
    return [elem for row in puzzle["matrix"] for elem in row] + [
        puzzle["reward"],
        puzzle["points"],
    ]


def state_to_vec(state: VisibleState) -> typing.List[int]:
    return (
        [elem for p in state["black_puzzles"] for elem in puzzle_to_vec(p)]
        + [elem for p in state["white_puzzles"] for elem in puzzle_to_vec(p)]
        + list(state["players_pieces"].values())
        + list(state["players_points"].values())
        + [
            elem
            for puzzles in state["players_puzzles"].values()
            for i in range(4)
            for elem in puzzle_to_vec(None if i >= len(puzzles) else puzzles[i])
        ]
        + [
            state["black_puzzles_remaining"],
            state["white_puzzles_remaining"],
            state["current_player"],
            state["remaining_actions"],
            1 if state["did_master_action"] else 0,
            state["points_to_pay"],
            0 if state["remaining_rounds"] is None else state["remaining_rounds"] + 2,
        ]
    )


def choose_action(
    brain: nn.Sequential, game: ProjectLGame
) -> typing.Optional[ActionData]:
    all_options = compute(game)

    if len(all_options) == 0:
        return None

    options_and_avaliations = [
        (action, brain(torch.tensor(state_to_vec(state), dtype=torch.float)))
        for action, state in all_options
    ]
    choosed_action = options_and_avaliations[0][0]
    choosed_avaliation = options_and_avaliations[0][1]
    for action, avaliation in options_and_avaliations:
        if avaliation > choosed_avaliation:
            choosed_avaliation = avaliation
            choosed_action = action

    return choosed_action


def get_random_brain(state_vec_len: int) -> nn.Sequential:
    return nn.Sequential(
        nn.Linear(state_vec_len, 96),
        nn.Tanh(),
        nn.Linear(96, 48),
        nn.Tanh(),
        nn.Linear(48, 1),
        nn.Identity(),
    )


def compare_brains(
    brain_1: nn.Sequential, brain_2: nn.Sequential, render=False, round_limit=1000
) -> typing.Tuple[int, int]:

    brains = [brain_1, brain_2]
    game = ProjectLGame()

    for round in range(round_limit):
        if render:
            game.render()
            print(
                f"======================================================= ROUND {round} ======================================================="
            )
        current_brain = brains[game.current_player]
        action = choose_action(current_brain, game)
        if action is None:
            break
        game.step(action)

    if render:
        print("Game has ended, points:")
        print(f"player 0: {game.players_points[0]}")
        print(f"player 1: {game.players_points[1]}")

    return game.players_points[0], game.players_points[1]


def brain_is_dummy(brain: nn.Sequential, render=False) -> bool:
    a, b = compare_brains(brain, brain, render=render, round_limit=20)
    return a == 0 and b == 0


def save_brain(brain: nn.Sequential) -> None:
    model_quantity = len(os.listdir("models"))
    torch.save(brain, f"models/brain_{model_quantity}.pkl")


def get_not_dummy_brain() -> nn.Sequential:
    while True:
        random_brain = get_random_brain(STATE_VEC_LEN)
        if not brain_is_dummy(random_brain):
            return random_brain


def get_and_save_not_dummy_brains(quantity: int) -> typing.List[nn.Sequential]:

    brains: typing.List[nn.Sequential] = []

    for _ in range(quantity):
        brain = get_not_dummy_brain()
        brains.append(brain)
        save_brain(brain)

    return brains


def load_brain(number: int) -> nn.Sequential:
    return torch.load(f"models/brain_{number}.pkl")


get_and_save_not_dummy_brains(94)
