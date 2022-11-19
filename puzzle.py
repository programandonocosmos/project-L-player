from piece import Piece
import typing

Point = typing.Tuple[int, int]
Row = typing.List[Point]
Matrix = typing.List[Row]


class PuzzleData(typing.TypedDict):
    matrix: Matrix
    points: int
    reward: int


class Puzzle:
    def __init__(self, matrix: Matrix, points: int, reward: Piece) -> None:
        self.matrix = matrix
        self.points = points
        self.reward = reward

    def extract_data(self) -> PuzzleData:
        return {
            "matrix": self.matrix,
            "points": self.points,
            "reward": self.reward.value,
        }


white_puzzles = [
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ],
        2,
        Piece.BLUE,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 0, 1],
        ],
        2,
        Piece.PURPLE,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ],
        2,
        Piece.RED,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
        ],
        3,
        Piece.LSHAPE,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
        ],
        3,
        Piece.BLUE,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1],
        ],
        1,
        Piece.GREEN,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 1, 1, 1, 1],
        ],
        0,
        Piece.LSHAPE,
    ),
]

black_puzzles = [
    Puzzle(
        [
            [1, 1, 0, 1, 1],
            [1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
        ],
        4,
        Piece.DOT,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ],
        4,
        Piece.GREEN,
    ),
    Puzzle(
        [
            [1, 1, 0, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ],
        4,
        Piece.CORNER,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        4,
        Piece.BLUE,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
        ],
        5,
        Piece.DOT,
    ),
]
