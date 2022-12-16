from projectl import (
    ProjectLGame,
    ActionEnum,
    Piece,
    Rotation,
    ActionData,
    VisibleState,
    piece_size,
)
from pydantic import ValidationError
import typing
import itertools


def compute_get_dot(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    action_data = {"action": ActionEnum.GET_DOT.value, "action_data": {}}
    fake_game = game.copy()
    try:
        visible_state, __, _ = fake_game.step(action_data)
        return [(action_data, visible_state)]
    except:
        return []


def compute_take_puzzle(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    output = []

    for p in range(8):
        action_data = {
            "action": ActionEnum.TAKE_PUZZLE.value,
            "action_data": {"which_puzzle": p},
        }
        fake_game = game.copy()
        try:
            visible_state, __, _ = fake_game.step(action_data)
            output.append((action_data, visible_state))
        except:
            pass

    return output


def compute_upgrade_piece(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    output = []

    for p1 in list(Piece):
        if game.players_pieces[(game.current_player, p1)] > 0:
            for p2 in list(Piece):
                if game.piece_quantity[p2] > 0:
                    action_data = {
                        "action": ActionEnum.UPGRADE_PIECE.value,
                        "action_data": {"from_piece": p1.value, "to_piece": p2.value},
                    }
                    fake_game = game.copy()
                    try:
                        visible_state, __, _ = fake_game.step(action_data)
                        output.append((action_data, visible_state))
                    except:
                        pass

    return output


def compute_place_piece(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    output = []

    for piece in list(Piece):
        if game.players_pieces[(game.current_player, piece)] > 0:
            for puzzle_num in range(len(game.players_puzzles[game.current_player])):
                puzzle = game.players_puzzles[game.current_player][puzzle]
                if (
                    len(
                        [
                            (x, y)
                            for x in range(5)
                            for y in range(5)
                            if puzzle.matrix[x][y] == 0
                        ]
                    )
                    >= piece_size[piece]
                ):
                    for x_coord in range(5):
                        for y_coord in range(5):
                            if puzzle.matrix[x_coord][y_coord] == 0:
                                for rot in list(Rotation):
                                    for rev in [False, True]:
                                        action_data = {
                                            "action": ActionEnum.PLACE_PIECE.value,
                                            "action_data": {
                                                "puzzle": puzzle_num,
                                                "piece": piece.value,
                                                "x_coord": x_coord,
                                                "y_coord": y_coord,
                                                "rotation": rot.value,
                                                "reversed": rev,
                                            },
                                        }
                                        fake_game = game.copy()
                                        try:
                                            visible_state, __, _ = fake_game.step(
                                                action_data
                                            )
                                            output.append((action_data, visible_state))
                                        except:
                                            pass

    return output


def compute_master(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    # UNFINISHED!!

    output = []

    if not game.did_master_action:
        all_pieces = [
            piece
            for (player_num, piece), quantity in game.players_pieces.items()
            if player_num == game.current_player
            for _ in range(quantity)
        ]
        puzzle_quantity = len(game.players_puzzles[game.current_player])
        if len(all_pieces) >= puzzle_quantity:
            for pieces in set(itertools.permutations(all_pieces, puzzle_quantity)):
                for puzzle_num, piece in enumerate(pieces):
                    puzzle = game.players_puzzles[game.current_player][puzzle]

    return output


def compute(game: ProjectLGame) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    output = [
        *compute_get_dot(game),
        *compute_take_puzzle(game),
        *compute_upgrade_piece(game),
        *compute_place_piece(game),
        *compute_master(game),
    ]

    return output
