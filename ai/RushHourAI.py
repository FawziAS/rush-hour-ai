from ai.AStar import AStar
from ai.BlockingHeuristic import BlockingHeuristic
from rush_hour.Board import Board


def main():
    initial_board = Board("A..RRRA..B.PXX.BCPQQQDCP..EDFFIIEHH.", BlockingHeuristic)
    AStar.start_a_star(initial_board, BlockingHeuristic)


if __name__ == "__main__":
    main()
