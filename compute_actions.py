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


def build_action_for_get_dot() -> ActionData:
    return {"action": ActionEnum.GET_DOT.value, "action_data": {}}


def build_action_for_take_puzzle(which_puzzle: int) -> ActionData:
    return {
        "action": ActionEnum.TAKE_PUZZLE.value,
        "action_data": {"which_puzzle": which_puzzle},
    }


def build_action_for_upgrade_piece(from_piece: Piece, to_piece: Piece) -> ActionData:
    return {
        "action": ActionEnum.UPGRADE_PIECE.value,
        "action_data": {"from_piece": from_piece.value, "to_piece": to_piece.value},
    }


def build_action_for_place_piece(
    puzzle: int, piece: Piece, x: int, y: int, rotation: Rotation, reversed: bool
) -> ActionData:
    return {
        "action": ActionEnum.PLACE_PIECE.value,
        "action_data": {
            "puzzle": puzzle,
            "piece": piece.value,
            "x_coord": x,
            "y_coord": y,
            "rotation": rotation.value,
            "reversed": reversed,
        },
    }


def build_action_for_master(
    place_piece_actions: typing.List[typing.Dict[str, typing.Any]]
) -> ActionData:
    return {
        "action": ActionEnum.MASTER.value,
        "action_data": {"place_piece_actions": place_piece_actions},
    }


def try_action(
    game: ProjectLGame, action_data: ActionData
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:
    fake_game = game.copy()
    try:
        visible_state, __, _ = fake_game.step(action_data)
        return [(action_data, visible_state)]
    except:
        return []


def compute_all_get_dot(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:
    return try_action(game, build_action_for_get_dot())


def compute_all_take_puzzle(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    return [
        res
        for i in range(8)
        for res in try_action(game, build_action_for_take_puzzle(i))
    ]


def compute_all_upgrade_piece(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    return [
        res
        for p1 in list(Piece)
        if game.players_pieces[(game.current_player, p1)] > 0
        for p2 in list(Piece)
        for res in try_action(game, build_action_for_upgrade_piece(p1, p2))
    ]


def compute_place_piece(
    game: ProjectLGame, piece: Piece, puzzle_num: int
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    if game.players_pieces[(game.current_player, piece)] <= 0:
        return []

    puzzle = game.players_puzzles[game.current_player][puzzle_num]

    if (
        len([(x, y) for x in range(5) for y in range(5) if puzzle.matrix[x][y] == 0])
        < piece_size[piece]
    ):
        return []

    return [
        res
        for x_coord in range(5)
        for y_coord in range(5)
        if puzzle.matrix[x_coord][y_coord] == 0
        for rot in list(Rotation)
        for rev in [False, True]
        for res in try_action(
            game,
            build_action_for_place_piece(puzzle_num, piece, x_coord, y_coord, rot, rev),
        )
    ]


def compute_all_place_piece(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    return [
        res
        for piece in list(Piece)
        if game.players_pieces[(game.current_player, piece)] > 0
        for puzzle_num in range(len(game.players_puzzles[game.current_player]))
        for res in compute_place_piece(game, piece, puzzle_num)
    ]


def compute_all_master(
    game: ProjectLGame,
) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    if game.did_master_action:
        return []

    all_pieces = [
        piece
        for (player_num, piece), quantity in game.players_pieces.items()
        if player_num == game.current_player
        for _ in range(quantity)
    ]
    puzzle_quantity = len(game.players_puzzles[game.current_player])

    if len(all_pieces) < puzzle_quantity:
        return []

    actions = [
        build_action_for_master(
            [
                act["action_data"]
                for puzzle_num, piece in enumerate(pieces)
                for act, _ in compute_place_piece(game, piece, puzzle_num)
            ]
        )
        for pieces in set(itertools.permutations(all_pieces, puzzle_quantity))
    ]

    return [res for action in actions for res in try_action(game, action)]


def compute(game: ProjectLGame) -> typing.List[typing.Tuple[ActionData, VisibleState]]:

    output = [
        *compute_all_get_dot(game),
        *compute_all_take_puzzle(game),
        *compute_all_upgrade_piece(game),
        *compute_all_place_piece(game),
        *compute_all_master(game),
    ]

    return output
