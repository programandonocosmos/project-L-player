from enum import Enum
import typing
from sty import bg


class Piece(Enum):
    DOT = 2
    GREEN = 3
    CORNER = 4
    BLUE = 5
    LSHAPE = 6
    PURPLE = 7
    TSHAPE = 8
    RED = 9
    LADDER = 10


class Rotation(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


piece_size = {
    Piece.DOT: 1,
    Piece.GREEN: 2,
    Piece.CORNER: 3,
    Piece.BLUE: 3,
    Piece.LSHAPE: 4,
    Piece.LADDER: 4,
    Piece.TSHAPE: 4,
    Piece.PURPLE: 4,
    Piece.RED: 4,
}

piece_color = {
    0: bg.white + "   " + bg.rs,
    1: bg.black + "   " + bg.rs,
    Piece.DOT.value: bg.yellow + "   " + bg.rs,
    Piece.GREEN.value: bg.green + "   " + bg.rs,
    Piece.CORNER.value: bg(255, 170, 50) + "   " + bg.rs,
    Piece.BLUE.value: bg.blue + "   " + bg.rs,
    Piece.LSHAPE.value: bg.cyan + "   " + bg.rs,
    Piece.LADDER.value: bg(255, 110, 50) + "   " + bg.rs,
    Piece.TSHAPE.value: bg(255, 0, 250) + "   " + bg.rs,
    Piece.PURPLE.value: bg(117, 85, 171) + "   " + bg.rs,
    Piece.RED.value: bg.red + "   " + bg.rs,
}

Point = typing.Tuple[int, int]
Points = typing.List[Point]
OrientationToPoints = typing.Dict[bool, Points]
RotationAndOrientationToPoints = typing.Dict[Rotation, OrientationToPoints]

reversable_pieces = [Piece.LSHAPE, Piece.LADDER]
undirectional_pieces = [Piece.DOT, Piece.RED]

piece_formats: typing.Dict[Piece, RotationAndOrientationToPoints] = {
    Piece.DOT: {
        Rotation.UP: {False: [(0, 0)], True: [(0, 0)]},
        Rotation.LEFT: {False: [(0, 0)], True: [(0, 0)]},
        Rotation.DOWN: {False: [(0, 0)], True: [(0, 0)]},
        Rotation.RIGHT: {False: [(0, 0)], True: [(0, 0)]},
    },
    Piece.GREEN: {
        Rotation.UP: {
            False: [(0, 0), (0, -1)],
            True: [(0, 0), (0, -1)],
        },
        Rotation.LEFT: {
            False: [(0, 0), (-1, 0)],
            True: [(0, 0), (-1, 0)],
        },
        Rotation.DOWN: {
            False: [(0, 0), (0, 1)],
            True: [(0, 0), (0, 1)],
        },
        Rotation.RIGHT: {
            False: [(0, 0), (1, 0)],
            True: [(0, 0), (1, 0)],
        },
    },
    Piece.BLUE: {
        Rotation.UP: {
            False: [
                (0, 0),
                (0, -1),
                (0, -2),
            ],
            True: [
                (0, 0),
                (0, -1),
                (0, -2),
            ],
        },
        Rotation.LEFT: {
            False: [
                (0, 0),
                (-1, 0),
                (-2, 0),
            ],
            True: [
                (0, 0),
                (-1, 0),
                (-2, 0),
            ],
        },
        Rotation.DOWN: {
            False: [
                (0, 0),
                (0, 1),
                (0, 2),
            ],
            True: [
                (0, 0),
                (0, 1),
                (0, 2),
            ],
        },
        Rotation.RIGHT: {
            False: [
                (0, 0),
                (1, 0),
                (2, 0),
            ],
            True: [
                (0, 0),
                (1, 0),
                (2, 0),
            ],
        },
    },
    Piece.CORNER: {
        Rotation.UP: {
            False: [
                (0, 0),
                (0, 1),
                (-1, 0),
            ],
            True: [
                (0, 0),
                (0, 1),
                (-1, 0),
            ],
        },
        Rotation.LEFT: {
            False: [
                (0, 0),
                (-1, 0),
                (0, -1),
            ],
            True: [
                (0, 0),
                (-1, 0),
                (0, -1),
            ],
        },
        Rotation.DOWN: {
            False: [
                (0, 0),
                (0, -1),
                (1, 0),
            ],
            True: [
                (0, 0),
                (0, -1),
                (1, 0),
            ],
        },
        Rotation.RIGHT: {
            False: [
                (0, 0),
                (1, 0),
                (0, 1),
            ],
            True: [
                (0, 0),
                (1, 0),
                (0, 1),
            ],
        },
    },
    Piece.TSHAPE: {
        Rotation.UP: {
            False: [
                (0, 0),
                (1, 0),
                (1, 1),
                (2, 0),
            ],
            True: [
                (0, 0),
                (1, 0),
                (1, 1),
                (2, 0),
            ],
        },
        Rotation.LEFT: {
            False: [
                (0, 0),
                (0, 1),
                (-1, 1),
                (0, 2),
            ],
            True: [
                (0, 0),
                (0, 1),
                (-1, 1),
                (0, 2),
            ],
        },
        Rotation.DOWN: {
            False: [
                (0, 0),
                (-1, 0),
                (-1, -1),
                (-2, 0),
            ],
            True: [
                (0, 0),
                (-1, 0),
                (-1, -1),
                (-2, 0),
            ],
        },
        Rotation.RIGHT: {
            False: [
                (0, 0),
                (0, -1),
                (1, -1),
                (0, -2),
            ],
            True: [
                (0, 0),
                (0, -1),
                (1, -1),
                (0, -2),
            ],
        },
    },
    Piece.PURPLE: {
        Rotation.UP: {
            False: [
                (0, 0),
                (0, -1),
                (0, -2),
                (0, -3),
            ],
            True: [
                (0, 0),
                (0, -1),
                (0, -2),
                (0, -3),
            ],
        },
        Rotation.LEFT: {
            False: [
                (0, 0),
                (-1, 0),
                (-2, 0),
                (-3, 0),
            ],
            True: [
                (0, 0),
                (-1, 0),
                (-2, 0),
                (-3, 0),
            ],
        },
        Rotation.DOWN: {
            False: [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
            ],
            True: [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
            ],
        },
        Rotation.RIGHT: {
            False: [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
            ],
            True: [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
            ],
        },
    },
    Piece.RED: {
        Rotation.UP: {
            False: [
                (0, 0),
                (0, 1),
                (-1, 0),
                (-1, 1),
            ],
            True: [
                (0, 0),
                (0, 1),
                (-1, 0),
                (-1, 1),
            ],
        },
        Rotation.LEFT: {
            False: [
                (0, 0),
                (0, 1),
                (-1, 0),
                (-1, 1),
            ],
            True: [
                (0, 0),
                (0, 1),
                (-1, 0),
                (-1, 1),
            ],
        },
        Rotation.DOWN: {
            False: [
                (0, 0),
                (0, 1),
                (-1, 0),
                (-1, 1),
            ],
            True: [
                (0, 0),
                (0, 1),
                (-1, 0),
                (-1, 1),
            ],
        },
        Rotation.RIGHT: {
            False: [
                (0, 0),
                (0, 1),
                (-1, 0),
                (-1, 1),
            ],
            True: [
                (0, 0),
                (0, 1),
                (-1, 0),
                (-1, 1),
            ],
        },
    },
    Piece.LSHAPE: {
        Rotation.UP: {
            False: [
                (0, 0),
                (0, 1),
                (0, 2),
                (1, 0),
            ],
            True: [
                (0, 0),
                (0, 1),
                (0, 2),
                (-1, 0),
            ],
        },
        Rotation.LEFT: {
            False: [
                (0, 0),
                (-1, 0),
                (-2, 0),
                (0, 1),
            ],
            True: [
                (0, 0),
                (-1, 0),
                (-2, 0),
                (0, -1),
            ],
        },
        Rotation.DOWN: {
            False: [
                (0, 0),
                (0, -1),
                (0, -2),
                (-1, 0),
            ],
            True: [
                (0, 0),
                (0, -1),
                (0, -2),
                (1, 0),
            ],
        },
        Rotation.RIGHT: {
            False: [
                (0, 0),
                (1, 0),
                (2, 0),
                (0, -1),
            ],
            True: [
                (0, 0),
                (1, 0),
                (2, 0),
                (0, 1),
            ],
        },
    },
    Piece.LADDER: {
        Rotation.UP: {
            False: [
                (0, 0),
                (0, 1),
                (1, 1),
                (1, 2),
            ],
            True: [
                (0, 0),
                (0, 1),
                (-1, 1),
                (-1, 2),
            ],
        },
        Rotation.LEFT: {
            False: [
                (0, 0),
                (-1, 0),
                (-1, 1),
                (-2, 1),
            ],
            True: [
                (0, 0),
                (-1, 0),
                (-1, -1),
                (-2, -1),
            ],
        },
        Rotation.DOWN: {
            False: [
                (0, 0),
                (0, -1),
                (-1, -1),
                (-1, -2),
            ],
            True: [
                (0, 0),
                (0, -1),
                (1, -1),
                (1, -2),
            ],
        },
        Rotation.RIGHT: {
            False: [
                (0, 0),
                (1, 0),
                (1, -1),
                (2, -1),
            ],
            True: [
                (0, 0),
                (1, 0),
                (1, 1),
                (2, 1),
            ],
        },
    },
}
