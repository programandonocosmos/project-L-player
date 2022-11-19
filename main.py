import typing
from piece import Piece
from puzzle import white_puzzles, black_puzzles, Puzzle, PuzzleData
import random


class VisibleState(typing.TypedDict):
    black_puzzles: typing.List[PuzzleData]
    white_puzzles: typing.List[PuzzleData]
    black_puzzles_left: int
    white_puzzles_left: int
    piece_quantity: typing.Dict[int, int]
    players_pieces: typing.Dict[typing.Tuple[int, int], int]
    players_points: typing.Dict[int, int]
    current_player: int
    remaining_actions: int
    did_master_action: bool


class ProjectLGame:
    def __init__(self, player_quantity: int = 2) -> None:
        self.player_quantity = player_quantity
        self.black_puzzle_quantity = {2: 12, 3: 14, 4: 16}[player_quantity]
        self.reset()

    def reset(self):
        self.piece_quantity: typing.Dict[Piece, int] = {
            {piece: 15} for piece in list(Piece)
        }
        shuffled_black_puzzles: typing.List[Puzzle] = random.shuffle(black_puzzles)
        shuffled_white_puzzles: typing.List[Puzzle] = random.shuffle(white_puzzles)
        self.black_puzzles = shuffled_black_puzzles[:4]
        self.white_puzzles = shuffled_white_puzzles[:4]
        self.black_puzzles_left = shuffled_black_puzzles[4 : self.black_puzzle_quantity]
        self.white_puzzles_left = shuffled_white_puzzles[4:32]
        self.players_pieces = {
            (player_num, piece): 1 if piece in [Piece.DOT, Piece.GREEN] else 0
            for piece in list(Piece)
            for player_num in range(self.player_quantity)
        }
        self.players_points = {
            player_num: 0 for player_num in range(self.player_quantity)
        }
        self.current_player: int = 0
        self.remaining_actions: int = 3
        self.did_master_action: bool = False

    def extract_state(self) -> VisibleState:
        return {
            "black_puzzles": [p.extract_data() for p in self.black_puzzles],
            "white_puzzles": [p.extract_data() for p in self.white_puzzles],
            "black_puzzles_left": [p.extract_data() for p in self.black_puzzles_left],
            "white_puzzles_left": [p.extract_data() for p in self.white_puzzles_left],
            "piece_quantity": {p.value: q for p, q in self.piece_quantity.items()},
            "players_pieces": {
                (pl, pi.value): q for (pl, pi), q in self.players_pieces.items()
            },
            "players_points": self.players_points,
            "current_player": self.current_player,
            "remaining_actions": self.remaining_actions,
            "did_master_action": self.did_master_action,
        }

    def step(self):
        pass

    def render(self):
        pass
