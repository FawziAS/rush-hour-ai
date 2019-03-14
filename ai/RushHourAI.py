import time

from ai.algorithms.AStar import AStar
from ai.heuristics.BlockingHeuristic import BlockingHeuristic
from ai.heuristics.MinimumDistanceHeuristic import MinimumDistanceHeuristic
from rush_hour.Board import Board


def main():
    global input_file
    try:
        FILE_PATH = "PUT input.txt FILE PATH HERE"
        input_file = open(FILE_PATH, 'r')
        inputs = input_file.readlines()
        problem_counter = 1
        for board_str in inputs:
            print("Problem " + str(problem_counter))
            starting_timestamp = int(time.time())
            initial_board = Board(board_str)
            initial_board.print_board()
            AStar.start_a_star(initial_board, MinimumDistanceHeuristic)
            finishing_timestamp = int(time.time())
            print("Time to solve: " + str(finishing_timestamp - starting_timestamp) + " seconds.")
            AStar.reset()
            problem_counter += 1
            print("----------------------------------------")
        input_file.close()
    except:
        print("Failed to open file.")


if __name__ == "__main__":
    main()
