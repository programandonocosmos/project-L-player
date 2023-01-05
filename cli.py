from projectl_old import ProjectLGame, ActionEnum, Piece, Rotation
from pydantic import ValidationError

game = ProjectLGame(2)

while True:
    game.render()
    print("------------------")
    print("choose an action:")
    for action in list(ActionEnum):
        print(f"- {action.value}) {action.name}")
    action_number = int(input("enter a number: "))

    try:
        if action_number == ActionEnum.GET_DOT.value:
            game.step({"action": ActionEnum.GET_DOT.value, "action_data": {}})
        elif action_number == ActionEnum.UPGRADE_PIECE.value:
            for piece in list(Piece):
                print(f"- {piece.value}) {piece.name}")
            from_piece = int(input("from piece: "))
            to_piece = int(input("to piece: "))
            game.step(
                {
                    "action": ActionEnum.UPGRADE_PIECE.value,
                    "action_data": {"from_piece": from_piece, "to_piece": to_piece},
                }
            )
        elif action_number == ActionEnum.TAKE_PUZZLE.value:
            puzzle_number = int(input("puzzle number: "))
            game.step(
                {
                    "action": ActionEnum.TAKE_PUZZLE.value,
                    "action_data": {"which_puzzle": puzzle_number},
                }
            )
        elif action_number == ActionEnum.PLACE_PIECE.value:
            puzzle_number = int(input("puzzle number: "))
            for piece in list(Piece):
                print(f"- {piece.value}) {piece.name}")
            piece_number = int(input("piece number: "))
            x_coord = int(input("x position: "))
            y_coord = int(input("y position: "))
            for rot in list(Rotation):
                print(f"- {rot.value}) {rot.name}")
            rotation = int(input("rotation: "))
            print("- 1) True")
            print("- 2) False")
            reversed = input("reversed: ") == "1"
            game.step(
                {
                    "action": ActionEnum.PLACE_PIECE.value,
                    "action_data": {
                        "puzzle": puzzle_number,
                        "piece": piece_number,
                        "x_coord": x_coord,
                        "y_coord": y_coord,
                        "rotation": rotation,
                        "reversed": reversed,
                    },
                }
            )
        elif action_number == ActionEnum.MASTER.value:
            actions = []
            for puzzle_number in range(len(game.players_puzzles[game.current_player])):
                for piece in list(Piece):
                    print(f"- {piece.value}) {piece.name}")
                piece_number = int(input("piece number: "))
                x_coord = int(input("x position: "))
                y_coord = int(input("y position: "))
                for rot in list(Rotation):
                    print(f"- {rot.value}) {rot.name}")
                rotation = int(input("rotation: "))
                print("- 1) True")
                print("- 2) False")
                reversed = input("reversed: ") == "1"
                actions.append(
                    {
                        "puzzle": puzzle_number,
                        "piece": piece_number,
                        "x_coord": x_coord,
                        "y_coord": y_coord,
                        "rotation": rotation,
                        "reversed": reversed,
                    }
                )
            game.step(
                {
                    "action": ActionEnum.MASTER.value,
                    "action_data": {"place_piece_actions": actions},
                }
            )
        elif action_number == ActionEnum.STOP.value:
            game.step({"action": ActionEnum.STOP.value, "action_data": {}})
    except (ProjectLGame.InvalidAction, ValidationError, ValueError) as e:
        print(e)
