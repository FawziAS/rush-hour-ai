import sys
import time

from ai.algorithms.AStar import AStar
from ai.heuristics.BlockingHeuristic import BlockingHeuristic
from ai.heuristics.MinimumDistanceHeuristic import MinimumDistanceHeuristic
from ai.heuristics.ZeroHeuristic import ZeroHeuristic
from rush_hour.Board import Board


def main():
    global input_file
    if len(sys.argv) < 3:
        raise Exception("Missing commandline arguments. Should have input.txt path and TimeLimit.")

    try:
        FILE_PATH = sys.argv[1]
        FILE_PATH = FILE_PATH.replace("\\", "\\\\")
        time_limit = sys.argv[2]
        input_file = open(FILE_PATH, 'r')
        inputs = input_file.readlines()
        problem_counter = 1
        for board_str in inputs:
            print("Problem " + str(problem_counter))
            initial_board = Board(board_str)
            initial_board.print_board()
            AStar.start_a_star(initial_board, BlockingHeuristic, time_limit)
            print(AStar.get_game_info())
            AStar.reset()
            problem_counter += 1
            print("----------------------------------------")
        input_file.close()
    except:
        print("Failed to open file.")


if __name__ == "__main__":
    main()
