from enum import Enum


class Piece(Enum):
    DOT = 1
    GREEN = 2
    CORNER = 3
    BLUE = 4
    LSHAPE = 5
    PURPLE = 6
    TSHAPE = 7
    RED = 8
    LADDER = 9


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
