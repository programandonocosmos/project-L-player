import typing
from piece import Piece, Rotation, piece_size, piece_formats
from puzzle import white_puzzles, black_puzzles, Puzzle, PuzzleData, print_puzzles
import random
from enum import Enum
from pydantic import BaseModel, validator
import typing


class VisibleState(typing.TypedDict):
    black_puzzles: typing.List[typing.Optional[PuzzleData]]
    white_puzzles: typing.List[typing.Optional[PuzzleData]]
    black_puzzles_remaining: int
    white_puzzles_remaining: int
    players_pieces: typing.Dict[typing.Tuple[int, int], int]
    players_points: typing.Dict[int, int]
    players_puzzles: typing.Dict[int, typing.List[PuzzleData]]
    current_player: int
    remaining_actions: int
    did_master_action: bool
    remaining_rounds: typing.Optional[int]
    points_to_pay: int


class ActionData(typing.TypedDict):
    action: int
    action_data: typing.Dict[str, typing.Any]
