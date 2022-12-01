from enum import Enum
import typing


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

Point = typing.Tuple[int, int]
Points = typing.List[Point]
OrientationToPoints = typing.Dict[bool, Points]
RotationAndOrientationToPoints = typing.Dict[Rotation, OrientationToPoints]

piece_formats: typing.Dict[Piece, RotationAndOrientationToPoints] = {
    Piece.DOT: {
        Rotation.UP: {False: [(0, 0)], True: [(0, 0)]},
        Rotation.LEFT: {False: [(0, 0)], True: [(0, 0)]},
        Rotation.DOWN: {False: [(0, 0)], True: [(0, 0)]},
        Rotation.RIGHT: {False: [(0, 0)], True: [(0, 0)]},
    },
    Piece.GREEN: {
        Rotation.UP: {
            False: [(0, 0), (0, 1)],
            True: [(0, 0), (0, 1)],
        },
        Rotation.LEFT: {
            False: [(0, 0), (-1, 0)],
            True: [(0, 0), (-1, 0)],
        },
        Rotation.DOWN: {
            False: [(0, 0), (0, -1)],
            True: [(0, 0), (0, -1)],
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
                (1, 0),
                (2, 0),
            ],
            True: [
                (0, 0),
                (1, 0),
                (2, 0),
            ],
        },
        Rotation.LEFT: {
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
        Rotation.DOWN: {
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
        Rotation.RIGHT: {
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
        Rotation.LEFT: {
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
        Rotation.DOWN: {
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
        Rotation.RIGHT: {
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
                (-1, 0),
                (0, -1),
                (-1, -1),
            ],
            True: [
                (0, 0),
                (-1, 0),
                (0, -1),
                (-1, -1),
            ],
        },
        Rotation.DOWN: {
            False: [
                (0, 0),
                (0, -1),
                (1, 0),
                (1, -1),
            ],
            True: [
                (0, 0),
                (0, -1),
                (1, 0),
                (1, -1),
            ],
        },
        Rotation.RIGHT: {
            False: [
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1),
            ],
            True: [
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1),
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
