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
from ai.reinforcement_learning.PerceptronLearning import PerceptronLearning
from ai.utils.Difficulty import Difficulty
from rush_hour.Board import Board


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


def main():
    global input_file
    if len(sys.argv) < 3:
        raise Exception("Missing commandline arguments. Should have input.txt path and TimeLimit.")
    try:
        FILE_PATH = sys.argv[1]
        time_limit = int(sys.argv[2])
        input_file = open(FILE_PATH, 'r')
        goals_file = open("PUT GOALS.txt FILE HERE")
        solutions_file = open("PUT optimal_solutions.txt FILE PATH HERE")
        inputs = input_file.readlines()
        goals = goals_file.readlines()
        solutions = solutions_file.readlines()
        problem_counter = 1
        # taking each line in input and converting it to a Board object
        for i in range(len(inputs)):
            print("Problem " + str(problem_counter))
            board_difficulty = inputs[i].split(" ")
            initial_board = Board(board_difficulty[0])
            difficulty = get_difficulty(board_difficulty[1])
            goal_board = Board(goals[i])
            initial_board.print_board()
            # running AStar algorithm, to solve the current board.
            # AStar.start_a_star(initial_board, AdvancedBlockingHeuristic, time_limit, difficulty)
            # print(AStar.get_game_info())
            # AStar.reset()  # resetting the global variables and structures that AStar stores.
            # running IDAStar algorithm, to solve the current board.
            # IDAStar.start_idas(initial_board, UnblockingHeuristic, time_limit)
            # IDS.start_ids(initial_board, 40)
            # running BiDirectionalAStar algorithm, to solve the current board.
            BiDirectionalAStar.start_bidirectional_a_star(initial_board, goal_board, solutions[i], BlockingHeuristic,
                                                          150)
            # PerceptronLearning(initial_board, AdvancedBlockingHeuristic)
            problem_counter += 1
            print("----------------------------------------")
        input_file.close()
    except FileNotFoundError as e:
        logging.exception("Failed to open file.", e)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.print_stats(sort='cumulative')
