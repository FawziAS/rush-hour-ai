import sys

from ai.algorithms.AStar import AStar
from rush_hour.Board import Board, Direction
from rush_hour.Vehicle import Orientation


class PerceptronLearning:
    actions_dictionary = {}

    def __init__(self, initial_board, heuristic, time_limit):
        vehicles = initial_board.get_vehicles_on_board()
        optimal_solution_steps = self.get_a_star_solution(initial_board, heuristic, time_limit)
        for depth in range(len(optimal_solution_steps)):
            for vehicle in vehicles:
                if vehicle.get_orientation() == Orientation.HORIZONTAL:
                    for i in range(initial_board.get_board_size() + 1):
                        self.actions_dictionary.update({str(depth) + vehicle.get_name() + "L" + str(i): 0})
                        self.actions_dictionary.update({str(depth) + vehicle.get_name() + "R" + str(i): 0})
                else:
                    for i in range(initial_board.get_board_size() + 1):
                        self.actions_dictionary.update({str(depth) + vehicle.get_name() + "U" + str(i): 0})
                        self.actions_dictionary.update({str(depth) + vehicle.get_name() + "D" + str(i): 0})

        self.train_the_agent(initial_board, optimal_solution_steps, time_limit)
        print("Perceptron solution: " + self.get_solution_from_dictionary(initial_board, optimal_solution_steps))
        # TODO: Print actions' weights.
        actions_weights = ""
        print(actions_weights)

    def get_a_star_solution(self, initial_board, heuristic, time_limit):
        board = Board(initial_board.get_board_str())
        if not AStar.start_a_star(board, heuristic, time_limit):
            AStar.reset()
            raise Exception("Couldn't find solution to train the agent")
        win_state = AStar.get_win_state()
        AStar.reset()
        a_star_solution = win_state.get_solution_path().strip() + " " + win_state.get_last_move()
        solution_steps = a_star_solution.strip().split(" ")
        return solution_steps

    def train_the_agent(self, initial_board, a_star_solution_steps, time_limit):
        a_star_solution = ""
        for step in a_star_solution_steps:
            a_star_solution += step + " "
        a_star_solution = a_star_solution.strip()
        perceptron_solution = ""
        while perceptron_solution != a_star_solution:
            board = Board(initial_board.get_board_str())
            perceptron_solution = self.learn_from_dictionary(board, a_star_solution_steps)
            perceptron_solution = perceptron_solution.strip()
            self.update_weights(a_star_solution_steps, perceptron_solution.split(" "))
        print("Done learning...\n")

    def learn_from_dictionary(self, board, solution_steps):
        possible_solution = ""
        min_step_value = sys.maxsize
        min_step = ""
        for i in range(len(solution_steps)):
            possible_steps = board.get_possible_steps()
            for step in possible_steps:
                if step != "" and (min_step_value > self.actions_dictionary.get(str(i) + step)):
                    min_step = step
                    min_step_value = self.actions_dictionary.get(str(i) + step)
            if not board.win_state():
                self.move_vehicle_from_step(board, min_step)
            possible_solution += min_step + " "
            min_step = ""
            min_step_value = sys.maxsize
        return possible_solution.strip()

    def move_vehicle_from_step(self, board, move):
        if move[1] == 'U':
            board.move_vehicle_on_board(move[0], Direction.UP, int(move[2]))
        if move[1] == 'D':
            board.move_vehicle_on_board(move[0], Direction.DOWN, int(move[2]))
        if move[1] == 'L':
            board.move_vehicle_on_board(move[0], Direction.LEFT, int(move[2]))
        if move[1] == 'R':
            board.move_vehicle_on_board(move[0], Direction.RIGHT, int(move[2]))

    def update_weights(self, a_star_solution_steps, perceptron_solution_steps):
        i = 0
        for action in a_star_solution_steps:
            step_value = self.actions_dictionary.get(str(i) + action)
            step_value -= 1
            self.actions_dictionary.update({str(i) + action: step_value})
            i += 1
        i = 0
        for action in perceptron_solution_steps:
            step_value = self.actions_dictionary.get(str(i) + action)
            step_value += 1
            self.actions_dictionary.update({str(i) + action: step_value})
            i += 1

        for i in range(len(a_star_solution_steps)):
            if a_star_solution_steps[i] == perceptron_solution_steps[i]:
                step_value = self.actions_dictionary.get(str(i) + perceptron_solution_steps[i])
                step_value -= 1
                self.actions_dictionary.update({str(i) + perceptron_solution_steps[i]: step_value})
            else:
                step_value = self.actions_dictionary.get(str(i) + perceptron_solution_steps[i])
                step_value += 1
                self.actions_dictionary.update({str(i) + perceptron_solution_steps[i]: step_value})

    def get_solution_from_dictionary(self, initial_board, solution_steps):
        board = Board(initial_board.get_board_str())
        possible_solution = ""
        min_step_value = sys.maxsize
        min_step = ""
        i = 0
        while not board.win_state():
            possible_steps = board.get_possible_steps()
            for step in possible_steps:
                if step != "" and (min_step_value > self.actions_dictionary.get(str(i) + step)):
                    min_step = step
                    min_step_value = self.actions_dictionary.get(str(i) + step)
            if not board.win_state():
                self.move_vehicle_from_step(board, min_step)
            possible_solution += min_step + " "
            min_step = ""
            min_step_value = sys.maxsize
            i += 1
        possible_solution += board.get_last_move()
        return possible_solution.strip()
