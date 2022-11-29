import typing
from piece import Piece, piece_size
from puzzle import white_puzzles, black_puzzles, Puzzle, PuzzleData, Matrix
import random
from enum import Enum


class VisibleState(typing.TypedDict):
    black_puzzles: typing.List[typing.Optional[PuzzleData]]
    white_puzzles: typing.List[typing.Optional[PuzzleData]]
    black_puzzles_remaining: int
    white_puzzles_remaining: int
    piece_quantity: typing.Dict[int, int]
    players_pieces: typing.Dict[typing.Tuple[int, int], int]
    players_points: typing.Dict[int, int]
    players_puzzles: typing.Dict[int, typing.List[PuzzleData]]
    current_player: int
    remaining_actions: int
    did_master_action: bool


class ActionEnum(Enum):
    TAKE_PUZZLE = 1
    GET_DOT = 2
    UPGRADE_PIECE = 3
    PLACE_PIECE = 4
    MASTER = 5


class TakeAction(typing.TypedDict):
    which_puzzle: int


class UpgradePieceAction(typing.TypedDict):
    from_piece: int
    to_piece: int


class PlacePieceAction(typing.TypedDict):
    puzzle: int
    new_matrix: Matrix


class MasterAction(typing.TypedDict):
    new_matrices: typing.List[Matrix]


class ActionData(typing.TypedDict):
    action: int
    action_data: typing.Optional[
        typing.Union[TakeAction, UpgradePieceAction, PlacePieceAction, MasterAction]
    ]


class ProjectLGame:
    class InvalidAction(Exception):
        pass

    def __init__(self, player_quantity: int = 2) -> None:
        self.player_quantity = player_quantity
        self.reset()

    def reset(self):
        self.piece_quantity = {
            piece: (
                15 - self.player_quantity if piece in [Piece.DOT, Piece.GREEN] else 15
            )
            for piece in list(Piece)
        }

        shuffled_black_puzzles = black_puzzles.copy()
        random.shuffle(shuffled_black_puzzles)

        shuffled_white_puzzles = white_puzzles.copy()
        random.shuffle(shuffled_white_puzzles)

        self.black_puzzles: typing.Sequence[
            typing.Optional[Puzzle]
        ] = shuffled_black_puzzles[:4]
        self.white_puzzles: typing.Sequence[
            typing.Optional[Puzzle]
        ] = shuffled_white_puzzles[:4]
        self.black_puzzles_remaining = shuffled_black_puzzles[4:20]
        self.white_puzzles_remaining = shuffled_white_puzzles[4:32]

        self.players_pieces = {
            (player_num, piece): 1 if piece in [Piece.DOT, Piece.GREEN] else 0
            for piece in list(Piece)
            for player_num in range(self.player_quantity)
        }
        self.players_points = {
            player_num: 0 for player_num in range(self.player_quantity)
        }
        self.players_puzzles: typing.Dict[int, typing.List[Puzzle]] = {
            player_num: [] for player_num in range(self.player_quantity)
        }
        self.current_player: int = 0
        self.remaining_actions: int = 3
        self.did_master_action: bool = False

    def extract_state(self) -> VisibleState:
        return {
            "black_puzzles": [
                p.extract_data() if p is not None else None for p in self.black_puzzles
            ],
            "white_puzzles": [
                p.extract_data() if p is not None else None for p in self.white_puzzles
            ],
            "black_puzzles_remaining": len(self.black_puzzles_remaining),
            "white_puzzles_remaining": len(self.white_puzzles_remaining),
            "piece_quantity": {p.value: q for p, q in self.piece_quantity.items()},
            "players_pieces": {
                (pl, pi.value): q for (pl, pi), q in self.players_pieces.items()
            },
            "players_points": self.players_points,
            "players_puzzles": {
                p: [pu.extract_data() for pu in pus]
                for p, pus in self.players_puzzles.items()
            },
            "current_player": self.current_player,
            "remaining_actions": self.remaining_actions,
            "did_master_action": self.did_master_action,
        }

    def get_dot(self) -> None:

        if self.piece_quantity[Piece.DOT] == 0:
            raise ProjectLGame.InvalidAction("There are no more DOT pieces")

        self.piece_quantity[Piece.DOT] -= 1
        self.players_pieces[(self.current_player, Piece.DOT)] += 1

    def upgrade_piece(self, action_data: UpgradePieceAction) -> None:

        from_piece = Piece(action_data["from_piece"])
        to_piece = Piece(action_data["to_piece"])

        if self.players_pieces[(self.current_player, from_piece)] == 0:
            raise ProjectLGame.InvalidAction(
                "You cannot upgrade a piece that you doesn't have"
            )

        if self.piece_quantity[to_piece] == 0:
            raise ProjectLGame.InvalidAction(
                "You cannot upgrade a piece that are not in the game storage"
            )

        from_piece_size = piece_size[from_piece]
        to_piece_size = piece_size[to_piece]

        if from_piece_size != to_piece_size and from_piece_size + 1 != to_piece_size:
            raise ProjectLGame.InvalidAction(
                "You are not upgrading piece size correctly"
            )

        self.players_pieces[(self.current_player, from_piece)] -= 1
        self.players_pieces[(self.current_player, to_piece)] += 1
        self.piece_quantity[from_piece] += 1
        self.piece_quantity[to_piece] -= 1

    def get_puzzle(self, action_data: TakeAction) -> None:
        pass

    def step(self, action: ActionData) -> typing.Tuple[VisibleState, int, bool]:
        if action["action"] == ActionEnum.GET_DOT.value:

            self.get_dot()

        if action["action"] == ActionEnum.UPGRADE_PIECE.value:

            if action["action_data"] is None:
                raise ProjectLGame.InvalidAction(
                    "Missing action data for UPGRADE_PIECE action"
                )

            if (
                action["action_data"].get("from_piece") is None
                or action["action_data"].get("to_piece") is None
            ):
                raise ProjectLGame.InvalidAction(
                    "Missing from_piece or to_piece for UPGRADE_PIECE action"
                )

            self.upgrade_piece(typing.cast(UpgradePieceAction, action["action_data"]))

        if action["action"] == ActionEnum.TAKE_PUZZLE.value:

            if action["action_data"] is None:
                raise ProjectLGame.InvalidAction(
                    "Missing action data for TAKE_PUZZLE action"
                )

            if action["action_data"].get("which_puzzle") is None:
                raise ProjectLGame.InvalidAction(
                    "Missing which_puzzle for TAKE_PUZZLE action"
                )

            self.get_puzzle(typing.cast(TakeAction, action["action_data"]))

        else:
            raise ProjectLGame.InvalidAction(f"Invalid action: {action['action']}")

        self.remaining_actions -= 1
        if self.remaining_actions == 0:

            self.remaining_actions = 3
            self.did_master_action = False
            self.current_player += 1
        if self.current_player == self.player_quantity:
            self.current_player = 0

        return self.extract_state(), self.players_points[self.current_player], True

    def render(self):
        pass
