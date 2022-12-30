from projectl import (
    ProjectLGame,
    ActionEnum,
    Piece,
    Rotation,
    ActionData,
    VisibleState,
    piece_size,
    Puzzle,
)
from piece import undirectional_pieces, reversable_pieces
import typing
import itertools
from dataclasses import dataclass, field

Row = typing.Tuple[int, ...]
Matrix = typing.Tuple[Row, ...]
Possibility = typing.Tuple[ActionData, VisibleState]
Possibilities = typing.List[Possibility]

PlacePieceParams = typing.Tuple[int, int, Rotation, bool]


@dataclass
class MemoizationStruct:
    puzzle_and_piece_memory: typing.Dict[
        typing.Tuple[Piece, Matrix], typing.List[PlacePieceParams]
    ]
    master_action_memory: typing.Dict[
        typing.Tuple[typing.Tuple[int, ...], typing.Tuple[Matrix, ...]],
        typing.List[ActionData],
    ]

    @staticmethod
    def new() -> "MemoizationStruct":
        return MemoizationStruct(puzzle_and_piece_memory={}, master_action_memory={})


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


def get_empty_position(
    game: ProjectLGame,
    action: ActionData,
    puzzles: typing.List[typing.Optional[Puzzle]],
) -> typing.List[int]:
    return (
        []
        if game.remaining_rounds != 1
        else (
            [i for i, puzzle in enumerate(puzzles) if puzzle is None]
            + (
                []
                if action["action"] != ActionEnum.TAKE_PUZZLE
                else [action["action_data"]["which_puzzle"]]
            )
        )
    )


def try_action(game: ProjectLGame, action_data: ActionData) -> Possibilities:
    fake_game = game.copy()
    empty_white_positions = get_empty_position(
        fake_game, action_data, fake_game.white_puzzles
    )
    empty_black_positions = get_empty_position(
        fake_game, action_data, fake_game.black_puzzles
    )

    try:
        visible_state, __, _ = fake_game.step(action_data)
    except Exception as e:
        return []

    modified_visible_state = visible_state.copy()

    modified_visible_state["black_puzzles"] = [
        None if i in empty_black_positions else p
        for i, p in enumerate(visible_state["black_puzzles"])
    ]

    modified_visible_state["white_puzzles"] = [
        None if i in empty_white_positions else p
        for i, p in enumerate(visible_state["white_puzzles"])
    ]
    return [(action_data, modified_visible_state)]


def compute_all_get_dot(game: ProjectLGame) -> Possibilities:
    return try_action(game, build_action_for_get_dot())


def compute_all_take_puzzle(game: ProjectLGame) -> Possibilities:

    return [
        res
        for i in range(8)
        for res in try_action(game, build_action_for_take_puzzle(i))
    ]


def compute_all_upgrade_piece(game: ProjectLGame) -> Possibilities:

    return [
        res
        for p1 in list(Piece)
        if game.players_pieces[(game.current_player, p1)] > 0
        for p2 in list(Piece)
        for res in try_action(game, build_action_for_upgrade_piece(p1, p2))
    ]


def compute_place_piece(
    game: ProjectLGame, piece: Piece, puzzle_num: int, mem: MemoizationStruct
) -> Possibilities:

    if game.players_pieces[(game.current_player, piece)] <= 0:
        return []

    puzzle = game.players_puzzles[game.current_player][puzzle_num]

    parsed_matrix = tuple(tuple(row) for row in puzzle.matrix)

    if mem.puzzle_and_piece_memory.get((piece, parsed_matrix)) is not None:
        return [
            res
            for x, y, rot, rev in mem.puzzle_and_piece_memory[(piece, parsed_matrix)]
            for res in try_action(
                game,
                build_action_for_place_piece(puzzle_num, piece, x, y, rot, rev),
            )
        ]

    if (
        len([(x, y) for x in range(5) for y in range(5) if puzzle.matrix[x][y] == 0])
        < piece_size[piece]
    ):
        return []

    possibilities = [
        res
        for x_coord in range(5)
        for y_coord in range(5)
        if puzzle.matrix[x_coord][y_coord] == 0
        for rot in ([Rotation.UP] if piece in undirectional_pieces else list(Rotation))
        for rev in ([False] if piece not in reversable_pieces else [False, True])
        for res in try_action(
            game,
            build_action_for_place_piece(puzzle_num, piece, x_coord, y_coord, rot, rev),
        )
    ]
    mem.puzzle_and_piece_memory[(piece, parsed_matrix)] = [
        (
            p[0]["action_data"]["x_coord"],
            p[0]["action_data"]["y_coord"],
            Rotation(p[0]["action_data"]["rotation"]),
            p[0]["action_data"]["reversed"],
        )
        for p in possibilities
    ]
    return possibilities


def compute_all_place_piece(
    game: ProjectLGame, mem: MemoizationStruct
) -> Possibilities:

    return [
        res
        for piece in list(Piece)
        if game.players_pieces[(game.current_player, piece)] > 0
        for puzzle_num in range(len(game.players_puzzles[game.current_player]))
        for res in compute_place_piece(game, piece, puzzle_num, mem)
    ]


def compute_all_master(game: ProjectLGame, mem: MemoizationStruct) -> Possibilities:

    if game.did_master_action:
        return []

    state = (
        tuple(
            game.players_pieces[(game.current_player, piece)] for piece in list(Piece)
        ),
        tuple(
            tuple(tuple(row) for row in p.matrix)
            for p in game.players_puzzles[game.current_player]
        ),
    )
    if mem.master_action_memory.get(state) is not None:
        actions = mem.master_action_memory[state]
        return [res for action in actions for res in try_action(game, action)]

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
        build_action_for_master([action["action_data"] for action in action_per_puzzle])
        for pieces in set(itertools.permutations(all_pieces, puzzle_quantity))
        for action_per_puzzle in itertools.product(
            *[
                [act for act, _ in compute_place_piece(game, piece, puzzle_num, mem)]
                for puzzle_num, piece in enumerate(pieces)
            ]
        )
    ]

    mem.master_action_memory[state] = actions

    return [res for action in actions for res in try_action(game, action)]


def compute(game: ProjectLGame, mem: MemoizationStruct) -> Possibilities:

    output = [
        *compute_all_get_dot(game),
        *compute_all_take_puzzle(game),
        *compute_all_upgrade_piece(game),
        *compute_all_place_piece(game, mem),
        *compute_all_master(game, mem),
    ]

    return output
