from ai.AStar import AStar
from ai.BlockingHeuristic import BlockingHeuristic
from rush_hour.Board import Board


def main():
    initial_board = Board("AAB.CCDDB..OPXX.EOPQQQEOPF.GHH.F.GII", BlockingHeuristic)
    initial_board.print_board()
    AStar.start_a_star(initial_board, BlockingHeuristic)


if __name__ == "__main__":
    main()
