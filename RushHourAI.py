import cProfile
import logging
import sys
from enum import Enum

from ai.algorithms.AStar import AStar
from ai.algorithms.BiDirectionalAStar import BiDirectionalAStar
from ai.algorithms.IDAStar import IDAStar
from ai.algorithms.IDS import IDS
from ai.heuristics.AdvancedBlockingHeuristic import AdvancedBlockingHeuristic
from ai.heuristics.BlockingHeuristic import BlockingHeuristic
from ai.heuristics.MinimumDistanceHeuristic import MinimumDistanceHeuristic
from ai.heuristics.UnblockingHeuristic import UnblockingHeuristic
from ai.reinforcement_learning.PerceptronLearning import PerceptronLearning
from ai.utils.Difficulty import Difficulty
from rush_hour.Board import Board, Direction


class Algorithm(Enum):
    ASTAR = 0
    IDASTAR = 1
    BIDIRECTIONAL = 2
    PERCEPRTON = 3


def get_difficulty(difficulty_str):
    if difficulty_str == "Beginner":
        return Difficulty.BEGINNER
    if difficulty_str == "Intermediate":
        return Difficulty.INTERMEDIATE
    if difficulty_str == "Advanced":
        return Difficulty.ADVANCED
    if difficulty_str == "Expert":
        return Difficulty.EXPERT
    return Difficulty.NOT_DEFINED


def get_heuristic(heuristic_str):
    if heuristic_str == "blocking":
        return BlockingHeuristic
    if heuristic_str == "advanced":
        return AdvancedBlockingHeuristic
    if heuristic_str == "unblocking":
        return UnblockingHeuristic
    # Default heuristic
    return AdvancedBlockingHeuristic


def main():
    global input_file
    global arg_time_limit
    global heuristic_used
    global goals
    use_difficulty = 0
    if len(sys.argv) < 3:
        raise Exception("Missing commandline arguments.")
    try:
        FILE_PATH = sys.argv[1]
        algorithm = int(sys.argv[2])
        if algorithm == Algorithm.PERCEPRTON.value:
            if len(sys.argv) == 3:
                heuristic_used = get_heuristic("")
            else:
                heuristic_used = get_heuristic(sys.argv[3])
        elif len(sys.argv) < 5:
            raise Exception("Missing commandline arguments.")
        else:
            heuristic_used = get_heuristic(sys.argv[3])
            arg_time_limit = int(sys.argv[4])
            if algorithm == Algorithm.ASTAR.value:
                if len(sys.argv) == 6:
                    use_difficulty = int(sys.argv[5])
            elif algorithm == Algorithm.BIDIRECTIONAL.value:
                if len(sys.argv) < 6:
                    raise Exception("Missing commandline arguments.")
                else:
                    goals_file = open(sys.argv[5], 'r')
                    goals = goals_file.readlines()

        input_file = open(FILE_PATH, 'r')
        inputs = input_file.readlines()

        # taking each line in input and converting it to a Board object
        for i in range(len(inputs)):
            print("Problem " + str(i + 1))
            board_difficulty = inputs[i].split(" ")
            initial_board = Board(board_difficulty[0])
            difficulty = get_difficulty(board_difficulty[1])
            initial_board.print_board()

            # running AStar algorithm, to solve the current board.
            if algorithm == Algorithm.ASTAR.value:
                if use_difficulty == 1:
                    run_astar(initial_board, heuristic_used, arg_time_limit, difficulty)
                else:
                    run_astar(initial_board, heuristic_used, arg_time_limit, Difficulty.NOT_DEFINED)

            # running IDAStar algorithm, to solve the current board.
            elif algorithm == Algorithm.IDASTAR.value:
                run_idastar(initial_board, heuristic_used, arg_time_limit)

            # running BiDirectionalAStar algorithm, to solve the current board.
            elif algorithm == Algorithm.BIDIRECTIONAL.value:
                goal_board = Board(goals[i])
                run_bidirectional(initial_board, goal_board, heuristic_used, arg_time_limit)

            # running perceptron algorithm, to solve the current board.
            elif algorithm == Algorithm.PERCEPRTON.value:
                run_perceptron(initial_board, heuristic_used)

            print("----------------------------------------")

        input_file.close()

    except FileNotFoundError as e:
        logging.exception("Failed to open file.", e)


def run_astar(initial_board, heuristic, time_limit, difficulty):
    AStar.start_a_star(initial_board, heuristic, time_limit, difficulty)
    print(AStar.get_game_info())
    AStar.reset()  # resetting the global variables and structures that AStar stores.


def run_idastar(initial_board, heuristic, time_limit):
    IDAStar.start_idas(initial_board, heuristic, time_limit)


def run_bidirectional(initial_board, goal_board, heuristic, time_limit):
    BiDirectionalAStar.start_bidirectional_a_star(initial_board, goal_board,
                                                  heuristic,
                                                  time_limit)


def run_perceptron(initial_board, heuristic):
    PerceptronLearning(initial_board, heuristic)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.print_stats(sort='cumulative')