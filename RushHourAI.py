import cProfile
import logging
import sys

from ai.algorithms.AStar import AStar
from ai.algorithms.BiDirectionalAStar import BiDirectionalAStar
from ai.algorithms.IDAStar import IDAStar
from ai.algorithms.IDS import IDS
from ai.heuristics.AdvancedBlockingHeuristic import AdvancedBlockingHeuristic
from ai.heuristics.BlockingHeuristic import BlockingHeuristic
from ai.heuristics.MinimumDistanceHeuristic import MinimumDistanceHeuristic
from ai.heuristics.UnblockingHeuristic import UnblockingHeuristic
from rush_hour.Board import Board


def main():
    global input_file
    if len(sys.argv) < 3:
        raise Exception("Missing commandline arguments. Should have input.txt path and TimeLimit.")
    try:
        FILE_PATH = sys.argv[1]
        time_limit = int(sys.argv[2])
        input_file = open(FILE_PATH, 'r')
        goals_file = open("Put solutions.txt file here!")
        inputs = input_file.readlines()
        goals = goals_file.readlines()
        problem_counter = 1
        # taking each line in input and converting it to a Board object
        for i in range(len(inputs)):
            print("Problem " + str(problem_counter))
            initial_board = Board(inputs[i])
            goal_board = Board(goals[i])
            initial_board.print_board()
            # running AStar algorithm, to solve the current board.
            # AStar.start_a_star(initial_board, AdvancedBlockingHeuristic, time_limit)
            # print(AStar.get_game_info())
            # AStar.reset()  # resetting the global variables and structures that AStar stores.
            # running IDAStar algorithm, to solve the current board.
            # IDAStar.start_idas(initial_board, BlockingHeuristic, time_limit)
            # IDS.start_ids(initial_board, 40)
            # running BiDirectionalAStar algorithm, to solve the current board.
            BiDirectionalAStar.start_bidirectional_a_star(initial_board, goal_board, BlockingHeuristic, 1000)
            problem_counter += 1
            print("----------------------------------------")
        input_file.close()
    except Exception as e:
        logging.exception("Failed to open file.", e)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.print_stats(sort='cumulative')
