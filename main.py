from compute_actions import compute
from projectl import ProjectLGame, Piece, Puzzle

game = ProjectLGame()

game.players_pieces[(0, Piece.LSHAPE)] = 1
game.players_pieces[(0, Piece.LADDER)] = 1
game.players_pieces[(0, Piece.CORNER)] = 1

game.players_puzzles[0] = [
    Puzzle(
        [
            [1, 1, 1, 1, 1],
            [3, 1, 1, 1, 1],
            [3, 0, 1, 1, 1],
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
]

possibilities = compute(game)

print(f"QUANTITY: {len(possibilities)}")

# for p, _ in possibilities:
#     print(p)
#     print("")
