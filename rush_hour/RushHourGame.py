from pip._vendor.distlib.compat import raw_input

from ai.heuristics.BlockingHeuristic import BlockingHeuristic
from rush_hour.Board import Board, Direction


def main():
    board = Board("..OAAP..OB.PXXOB.PKQQQ..KDDEF.GG.EF.", BlockingHeuristic)
    board.print_board()
    play_game_with_simple_interface(board)


def play_game_with_simple_interface(board):
    move = raw_input("How would you like to move the cars on board? Format: CarNameDirectionSteps: ")
    while move != "!":
        if move[1] == 'U':
            board.move_vehicle_on_board(move[0], Direction.UP, int(move[2]))
        if move[1] == 'D':
            board.move_vehicle_on_board(move[0], Direction.DOWN, int(move[2]))
        if move[1] == 'L':
            board.move_vehicle_on_board(move[0], Direction.LEFT, int(move[2]))
        if move[1] == 'R':
            board.move_vehicle_on_board(move[0], Direction.RIGHT, int(move[2]))
        board.print_board()
        if board.win_state():
            break
        else:
            move = raw_input("How would you like to move the cars on board? Format: CarNameDirectionSteps: ")
    if move == '!':
        print("Oops... Better luck next time :(")
    else:
        print("CONGRATS! You solved it!")


if __name__ == "__main__":
    main()
