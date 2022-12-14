from piece import Piece
import typing

Row = typing.List[int]
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

    def copy(self) -> "Puzzle":
        return Puzzle(
            [row.copy() for row in self.matrix],
            int(self.points),
            Piece(self.reward.value),
        )

    def __repr__(self) -> str:

        matrix_repr = ["", "", "", "", ""]
        for j in range(5):
            max_len = max(len(str(self.matrix[j][i])) for i in range(4, -1, -1))
            for i in range(4, -1, -1):
                matrix_repr[i] += (
                    " "
                    + str(self.matrix[j][i])
                    + " " * (max_len - len(str(self.matrix[j][i])))
                )

        matrix_repr_lst = "\n".join(matrix_repr)

        return (
            f"points: {self.points}\n"
            f"reward: {self.reward.name}\n"
            "matrix: \n"
            f"{matrix_repr_lst}"
        )


def print_puzzles(puzzles: typing.Sequence[typing.Optional[Puzzle]]) -> None:
    result = ["", "", "", "", "", "", "", "", ""]
    for puzzle in puzzles:
        if puzzle is None:
            for i in range(len(result)):
                result[i] += "|   None   "
        else:
            max_len = max(len(line) for line in str(puzzle).split("\n"))
            for i, line in enumerate(str(puzzle).split("\n")):
                result[i] += line + " " * (2 + max_len - len(line))
    print("\n".join(result))


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
            [1, 1, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 1, 1],
        ],
        5,
        Piece.DOT,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
        ],
        5,
        Piece.DOT,
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
            [1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ],
        4,
        Piece.GREEN,
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
            [1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        5,
        Piece.DOT,
    ),
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
            [0, 1, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
        ],
        3,
        Piece.LADDER,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 1, 1],
        ],
        3,
        Piece.PURPLE,
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
            [1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
        ],
        3,
        Piece.TSHAPE,
    ),
    Puzzle(
        [
            [1, 1, 0, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
        ],
        3,
        Piece.RED,
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
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0],
        ],
        4,
        Piece.BLUE,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0],
        ],
        3,
        Piece.GREEN,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
        ],
        3,
        Piece.CORNER,
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
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        4,
        Piece.CORNER,
    ),
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
        ],
        5,
        Piece.DOT,
    ),
]
