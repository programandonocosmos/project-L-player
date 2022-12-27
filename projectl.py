import typing
from piece import Piece, Rotation, piece_size, piece_formats
from puzzle import white_puzzles, black_puzzles, Puzzle, PuzzleData, print_puzzles
import random
from enum import Enum
from pydantic import BaseModel, validator

# USER INTERFACE (only default python types here)


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
    remaining_rounds: typing.Optional[int]
    points_to_pay: int


class ActionData(typing.TypedDict):
    action: int
    action_data: typing.Dict[str, typing.Any]


# INTERNAL TYPES (to make the code better)


class ActionEnum(Enum):
    TAKE_PUZZLE = 1
    GET_DOT = 2
    UPGRADE_PIECE = 3
    PLACE_PIECE = 4
    MASTER = 5
    STOP = 6


class CustomModel(BaseModel):
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class TakeAction(CustomModel):
    which_puzzle: int

    @validator("which_puzzle")
    def correct_range(cls, value: int) -> int:
        if value < 0 or value > 7:
            raise ValueError(f"{value} must be between 0 and 7")
        return value


class UpgradePieceAction(CustomModel):
    from_piece: Piece
    to_piece: Piece

    @validator("from_piece", "to_piece", pre=True)
    def parse_piece(cls, value: typing.Any) -> Piece:
        if value not in [p.value for p in list(Piece)]:
            raise ValueError(f"{value} not in {list(Piece)}")
        return Piece(value)


class PlacePieceAction(CustomModel):
    puzzle: int
    piece: Piece
    x_coord: int
    y_coord: int
    rotation: Rotation
    reversed: bool

    @validator("puzzle")
    def correct_puzzle_range(cls, value: int) -> int:
        if value < 0 or value > 7:
            raise ValueError(f"{value} must be between 0 and 7")
        return value

    @validator("piece", pre=True)
    def parse_piece(cls, value: typing.Any) -> Piece:
        if value not in [p.value for p in list(Piece)]:
            raise ValueError(f"{value} not in {list(Piece)}")
        return Piece(value)

    @validator("x_coord", "y_coord")
    def correct_coord_range(cls, value: int) -> int:
        if value < 0 or value > 4:
            raise ValueError(f"{value} must be between 0 and 4")
        return value

    @validator("rotation", pre=True)
    def parse_rotation(cls, value: typing.Any) -> Rotation:
        if value not in [p.value for p in list(Rotation)]:
            raise ValueError(f"{value} not in {list(Rotation)}")
        return Rotation(value)


class MasterAction(CustomModel):
    place_piece_actions: typing.List[PlacePieceAction]

    @validator("place_piece_actions", pre=True)
    def parse_actions(cls, value: typing.Any) -> typing.List[PlacePieceAction]:
        if not isinstance(value, list):
            raise ValueError(f"{value} is not a list")
        return [PlacePieceAction(**v) for v in value]


class ProjectLGame:
    class InvalidAction(Exception):
        pass

    def __init__(
        self, player_quantity: int = 2, state: typing.Optional["ProjectLGame"] = None
    ) -> None:
        self.player_quantity = player_quantity
        if state is None:
            self.reset()
        else:
            self.set_state(state)

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

        self.black_puzzles = typing.cast(
            typing.List[typing.Optional[Puzzle]], shuffled_black_puzzles[:4]
        )
        self.white_puzzles = typing.cast(
            typing.List[typing.Optional[Puzzle]], shuffled_white_puzzles[:4]
        )
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
        self.remaining_rounds: typing.Optional[int] = None
        self.points_to_pay: int = 0

    def set_state(self, state: "ProjectLGame") -> None:
        self.piece_quantity = {
            piece: piece_quantity
            for piece, piece_quantity in state.piece_quantity.items()
        }

        self.black_puzzles = [p if p is None else p.copy() for p in state.black_puzzles]
        self.white_puzzles = [p if p is None else p.copy() for p in state.white_puzzles]
        self.black_puzzles_remaining = state.black_puzzles_remaining.copy()
        self.white_puzzles_remaining = state.white_puzzles_remaining.copy()

        self.players_pieces = {
            (player_num, Piece(piece.value)): quantity
            for (player_num, piece), quantity in state.players_pieces.items()
        }
        self.players_points = {
            player_num: points for player_num, points in state.players_points.items()
        }
        self.players_puzzles = {
            player_num: [puzzle.copy() for puzzle in puzzles]
            for player_num, puzzles in state.players_puzzles.items()
        }
        self.current_player = int(state.current_player)
        self.remaining_actions = int(state.remaining_actions)
        self.did_master_action = bool(state.did_master_action)
        self.remaining_rounds = (
            None if state.remaining_rounds is None else int(state.remaining_rounds)
        )
        self.points_to_pay = int(state.points_to_pay)

    def copy(self) -> "ProjectLGame":
        return ProjectLGame(self.player_quantity, self)

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
            "remaining_rounds": self.remaining_rounds,
            "points_to_pay": self.points_to_pay,
        }

    def remove_done_puzzles(self) -> None:
        puzzles_to_remove = []
        for i, puzzle in enumerate(self.players_puzzles[self.current_player]):
            if all(v != 0 for row in puzzle.matrix for v in row):
                self.players_points[self.current_player] += puzzle.points
                if self.piece_quantity[puzzle.reward] > 0:
                    self.piece_quantity[puzzle.reward] -= 1
                    self.players_pieces[(self.current_player, puzzle.reward)] += 1
                all_positions = [v for row in puzzle.matrix for v in row]
                for piece in list(Piece):
                    piece_quantity_f = (
                        all_positions.count(piece.value) / piece_size[piece]
                    )
                    piece_quantity = int(piece_quantity_f)
                    if piece_quantity_f != piece_quantity:
                        raise ProjectLGame.InvalidAction(
                            f"Some internal error appeared: {puzzle.matrix}"
                        )
                    self.players_pieces[(self.current_player, piece)] += piece_quantity
                puzzles_to_remove.append(i)
        self.players_puzzles[self.current_player] = [
            p
            for p in self.players_puzzles[self.current_player]
            if p not in puzzles_to_remove
        ]

    def fill_table_with_puzzles(self) -> None:
        for i in range(len(self.black_puzzles)):
            if self.black_puzzles[i] is None and len(self.black_puzzles_remaining) > 0:
                self.black_puzzles[i] = self.black_puzzles_remaining.pop()

        for i in range(len(self.white_puzzles)):
            if self.white_puzzles[i] is None and len(self.white_puzzles_remaining) > 0:
                self.white_puzzles[i] = self.white_puzzles_remaining.pop()

    def get_dot(self) -> None:

        if self.piece_quantity[Piece.DOT] == 0:
            raise ProjectLGame.InvalidAction("There are no more DOT pieces")

        self.piece_quantity[Piece.DOT] -= 1
        self.players_pieces[(self.current_player, Piece.DOT)] += 1

    def upgrade_piece(self, action_data: UpgradePieceAction) -> None:

        from_piece = action_data.from_piece
        to_piece = action_data.to_piece

        if from_piece == to_piece:
            raise ProjectLGame.InvalidAction("You cannot upgrade a piece to itself")

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
                f"Bad piece upgrade ({from_piece_size} -> {to_piece_size})"
            )

        self.players_pieces[(self.current_player, from_piece)] -= 1
        self.players_pieces[(self.current_player, to_piece)] += 1
        self.piece_quantity[from_piece] += 1
        self.piece_quantity[to_piece] -= 1

    def get_puzzle(self, action_data: TakeAction) -> None:

        if len(self.players_puzzles[self.current_player]) == 4:
            raise ProjectLGame.InvalidAction("You can take only 4 puzzles")

        which_puzzle = action_data.which_puzzle
        is_black = 0 <= which_puzzle and which_puzzle <= 3
        is_white = 4 <= which_puzzle and which_puzzle <= 7
        puzzle_pos = which_puzzle % 4

        if is_black:
            puzzle = self.black_puzzles[puzzle_pos]
            if puzzle is None:
                raise ProjectLGame.InvalidAction(
                    "You cannot get a puzzle that doesn't exists"
                )

            self.players_puzzles[self.current_player].append(puzzle.copy())
            self.black_puzzles[puzzle_pos] = None

        elif is_white:
            puzzle = self.white_puzzles[puzzle_pos]
            if puzzle is None:
                raise ProjectLGame.InvalidAction(
                    "You cannot get a puzzle that doesn't exists"
                )

            self.players_puzzles[self.current_player].append(puzzle.copy())
            self.white_puzzles[puzzle_pos] = None

        else:
            raise ProjectLGame.InvalidAction(
                "You cannot get a puzzle that doesn't exists"
            )

    def place_piece(self, action_data: PlacePieceAction, only_try=False) -> None:

        if action_data.puzzle >= len(self.players_puzzles[self.current_player]):
            raise ProjectLGame.InvalidAction(
                "You cannot place a piece in a puzzle that doesn't exists"
            )

        puzzle = self.players_puzzles[self.current_player][action_data.puzzle]
        piece = action_data.piece
        rotation = action_data.rotation
        reversed = action_data.reversed
        x_coord = action_data.x_coord
        y_coord = action_data.y_coord

        if self.players_pieces[(self.current_player, piece)] == 0:
            raise ProjectLGame.InvalidAction(
                "You cannot place a piece that is not yours"
            )

        available_coords = [
            (i, j)
            for i, row in enumerate(puzzle.matrix)
            for j, value in enumerate(row)
            if value == 0
        ]

        piece_format = piece_formats[piece][rotation][reversed]
        necessary_coords = [(x_coord + x, y_coord + y) for x, y in piece_format]

        if not all(coord in available_coords for coord in necessary_coords):

            raise ProjectLGame.InvalidAction(
                "Cannot place a piece in a filled space "
                f"(necessary coords: {necessary_coords}, available coords: {available_coords})"
            )

        if not only_try:
            self.players_pieces[(self.current_player, piece)] -= 1
            for x, y in necessary_coords:
                puzzle.matrix[x][y] = piece.value

    def master_play(self, action_data: MasterAction) -> None:

        puzzles = [ac.puzzle for ac in action_data.place_piece_actions]
        pieces = [ac.piece for ac in action_data.place_piece_actions]
        remaining_pieces = [
            self.players_pieces[(self.current_player, p)] - pieces.count(p)
            for p in list(Piece)
        ]
        if any(r < 0 for r in remaining_pieces):
            raise ProjectLGame.InvalidAction(
                "Using more pieces then you have for MASTER action"
            )

        if len(self.players_puzzles[self.current_player]) == 0:
            raise ProjectLGame.InvalidAction("No puzzles for MASTER action")

        if len(puzzles) != len(set(puzzles)):
            raise ProjectLGame.InvalidAction("Repeated puzzle for MASTER action")

        if set(puzzles) != set(range(len(self.players_puzzles[self.current_player]))):
            raise ProjectLGame.InvalidAction("Missing puzzle for MASTER action")

        for ac in action_data.place_piece_actions:
            try:
                self.place_piece(ac, only_try=True)
            except ProjectLGame.InvalidAction as e:
                raise ProjectLGame.InvalidAction(f"{e} for MASTER action")

        self.did_master_action = True
        for ac in action_data.place_piece_actions:
            self.place_piece(ac)

    def step(self, action: ActionData) -> typing.Tuple[VisibleState, int, bool]:
        if self.remaining_rounds == -1:
            return self.extract_state(), self.players_points[self.current_player], False

        if self.remaining_rounds == 0:

            if action["action"] == ActionEnum.PLACE_PIECE.value:
                place_data = PlacePieceAction(**action["action_data"])
                self.place_piece(place_data)
                self.points_to_pay += 1

            elif action["action"] == ActionEnum.STOP.value:
                self.players_points[self.current_player] -= self.points_to_pay
                self.points_to_pay = 0
                self.remaining_actions = 0

        else:

            if action["action"] == ActionEnum.GET_DOT.value:
                self.get_dot()

            elif action["action"] == ActionEnum.UPGRADE_PIECE.value:
                upgrade_data = UpgradePieceAction(**action["action_data"])
                self.upgrade_piece(upgrade_data)

            elif action["action"] == ActionEnum.TAKE_PUZZLE.value:
                take_data = TakeAction(**action["action_data"])
                self.get_puzzle(take_data)

            elif action["action"] == ActionEnum.PLACE_PIECE.value:
                place_data = PlacePieceAction(**action["action_data"])
                self.place_piece(place_data)

            elif action["action"] == ActionEnum.MASTER.value:
                master_data = MasterAction(**action["action_data"])
                self.master_play(master_data)

            else:
                raise ProjectLGame.InvalidAction(f"Invalid action: {action['action']}")

            self.remaining_actions -= 1

        self.remove_done_puzzles()

        if self.remaining_actions == 0:

            self.remaining_actions = 3
            self.did_master_action = False
            self.current_player += 1

            self.fill_table_with_puzzles()

        if self.current_player == self.player_quantity:
            self.current_player = 0

        if len(self.black_puzzles_remaining) == 0:
            if self.remaining_rounds is None:
                self.remaining_rounds = 2
            elif self.current_player == 0:
                self.remaining_rounds -= 1

        if self.remaining_rounds == -1:
            return self.extract_state(), self.players_points[self.current_player], False

        return self.extract_state(), self.players_points[self.current_player], True

    def render(self):

        for player in range(self.player_quantity):
            playing = (
                "["
                + "X" * self.remaining_actions
                + " " * (3 - self.remaining_actions)
                + "]"
                if player == self.current_player
                else "[   ]"
            )
            print(f"{playing} PLAYER {player}")
            print(f"points: {self.players_points[player]}")
            print("pieces:")
            for piece in list(Piece):
                print(f"- {piece.name}: {self.players_pieces[(player, piece)]}")
            print("puzzles:")
            print_puzzles(self.players_puzzles[player])

        print("BLACK PUZZLES:")
        print(f"remaining: {len(self.black_puzzles_remaining)}")
        print_puzzles(self.black_puzzles)

        print("WHITE PUZZLES:")
        print(f"remaining: {len(self.white_puzzles_remaining)}")
        print_puzzles(self.white_puzzles)
