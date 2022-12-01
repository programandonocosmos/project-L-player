from enum import Enum


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
