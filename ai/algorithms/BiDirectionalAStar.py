import heapq
import time
from enum import Enum

from ai.algorithms.StateNode import StateNode
from ai.heuristics.AdvancedBlockingHeuristic import AdvancedBlockingHeuristic
from ai.heuristics.TotalDistanceHeuristic import TotalDistanceHeuristic


class Direction(Enum):
    FORWARD = 0
    BACKWARD = 1


class BiDirectionalAStar:
    opened_front = []
    opened_front_dictionary = {}
    opened_back = []
    opened_back_dictionary = {}
    closed_front = {}
    closed_back = {}

    @staticmethod
    def start_bidirectional_a_star(initial_state_representation, goal_state_representation, heuristic, time_limit):
        start_timestamp = float(time.time())
        initial_state = StateNode(initial_state_representation,
                                  heuristic.calculate_heuristic_value(initial_state_representation), 0)
        BiDirectionalAStar.initial_state_rep = initial_state_representation
        vehicles_on_initial_board = initial_state_representation.get_vehicles_on_board()
        goal_state = StateNode(goal_state_representation,
                               TotalDistanceHeuristic.calculate_heuristic_value(goal_state_representation,
                                                                                vehicles_on_initial_board), 0)

        # Added initial states
        heapq.heappush(BiDirectionalAStar.opened_front, initial_state)
        BiDirectionalAStar.opened_front_dictionary.update({initial_state_representation.get_board_str(): initial_state})
        heapq.heappush(BiDirectionalAStar.opened_back, goal_state)
        BiDirectionalAStar.opened_back_dictionary.update({goal_state_representation.get_board_str(): goal_state})

        while BiDirectionalAStar.opened_front and BiDirectionalAStar.opened_back:
            front_state = heapq.heappop(BiDirectionalAStar.opened_front)
            BiDirectionalAStar.opened_front_dictionary.pop(front_state.get_state_representation().get_board_str())
            BiDirectionalAStar.closed_front.update(
                {front_state.get_state_representation().get_board_str(): front_state})

            if front_state.get_state_representation().win_state():
                time_for_problem = float(time.time()) - start_timestamp
                print("Success in " + str(time_for_problem))
                print("Solution: " + front_state.get_state_representation().get_solution_path())
                BiDirectionalAStar.reset()
                return
            match_found = BiDirectionalAStar.connection_exists(front_state, Direction.FORWARD)
            if match_found is not None:
                time_for_problem = float(time.time()) - start_timestamp
                print("Success in " + str(time_for_problem))
                backwards_path = BiDirectionalAStar.backwards(
                    match_found.get_state_representation().get_solution_path())
                print("Solution: " + front_state.get_state_representation().get_solution_path() + backwards_path)
                BiDirectionalAStar.reset()
                return
            back_state = heapq.heappop(BiDirectionalAStar.opened_back)
            BiDirectionalAStar.opened_back_dictionary.pop(back_state.get_state_representation().get_board_str())
            BiDirectionalAStar.closed_back.update({back_state.get_state_representation().get_board_str(): back_state})
            match_found = BiDirectionalAStar.connection_exists(back_state, Direction.BACKWARD)
            if match_found is not None:
                time_for_problem = float(time.time()) - start_timestamp
                print("Success in " + str(time_for_problem))
                backwards_path = BiDirectionalAStar.backwards(back_state.get_state_representation().get_solution_path())
                print("Solution: " + match_found.get_state_representation().get_solution_path() + backwards_path)
                BiDirectionalAStar.reset()
                return

            front_neighbours = front_state.get_state_representation().get_neighbours()
            back_neighbours = back_state.get_state_representation().get_neighbours()

            BiDirectionalAStar.add_forward_relevant_states(front_neighbours, BiDirectionalAStar.opened_front,
                                                           BiDirectionalAStar.opened_front_dictionary,
                                                           BiDirectionalAStar.closed_front, heuristic,
                                                           front_state.get_depth())

            BiDirectionalAStar.add_backwards_relevant_states(back_neighbours, BiDirectionalAStar.opened_back,
                                                             BiDirectionalAStar.opened_back_dictionary,
                                                             BiDirectionalAStar.closed_back, TotalDistanceHeuristic,
                                                             back_state.get_depth(), vehicles_on_initial_board)
        print("Failed")
        return

    @staticmethod
    def connection_exists(state, search_direction):
        if search_direction == Direction.FORWARD:
            match = BiDirectionalAStar.opened_back_dictionary.get(state.get_state_representation().get_board_str())
            if match is not None:
                return match
            match = BiDirectionalAStar.closed_back.get(state.get_state_representation().get_board_str())
            if match is not None:
                return match
        else:
            match = BiDirectionalAStar.opened_front_dictionary.get(state.get_state_representation().get_board_str())
            if match is not None:
                return match
            match = BiDirectionalAStar.closed_front.get(state.get_state_representation().get_board_str())
            if match is not None:
                return match
        return None

    @staticmethod
    def add_forward_relevant_states(neighbour_states, opened, opened_dictionary, closed, heuristic, previous_depth):
        for state_representation in neighbour_states:
            heuristic_value = heuristic.calculate_heuristic_value(state_representation)
            opened_state = opened_dictionary.get(state_representation.get_board_str())
            # state is not in the open heap
            if opened_state is None:
                closed_state = closed.get(state_representation.get_board_str())
                # state wasn't visited before
                if closed_state is None:
                    # add it to the open heap
                    a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                    heapq.heappush(opened, a_star_node)
                    opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    continue
                else:
                    # state is in closed list
                    previous_heuristic_value = closed_state.get_heuristic_value()
                    # if current heuristic value is better, delete the old node from closed and add the current to open
                    if previous_heuristic_value > heuristic_value:
                        closed.pop(closed_state.get_board_representation().get_board_str())
                        a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                        heapq.heappush(opened, a_star_node)
                        opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    continue
            else:
                # state is in open list
                previous_heuristic_value = opened_state.get_heuristic_value()
                # heuristic value is better that the old one
                if previous_heuristic_value > heuristic_value:
                    # replace the old node with a new one with the new heuristic value in the open list
                    opened.remove(opened_state)
                    opened_dictionary.pop(opened_state.get_state_representation().get_board_str())
                    heapq.heapify(opened)
                    a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                    heapq.heappush(opened, a_star_node)
                    opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    continue
        return

    @staticmethod
    def add_backwards_relevant_states(neighbour_states, opened, opened_dictionary, closed, heuristic, previous_depth,
                                      vehicle_on_initial_board):
        for state_representation in neighbour_states:
            heuristic_value = heuristic.calculate_heuristic_value(state_representation, vehicle_on_initial_board)
            opened_state = opened_dictionary.get(state_representation.get_board_str())
            # state is not in the open heap
            if opened_state is None:
                closed_state = closed.get(state_representation.get_board_str())
                # state wasn't visited before
                if closed_state is None:
                    # add it to the open heap
                    a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                    heapq.heappush(opened, a_star_node)
                    opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    continue
                else:
                    # state is in closed list
                    previous_heuristic_value = closed_state.get_heuristic_value()
                    # if current heuristic value is better, delete the old node from closed and add the current to open
                    if previous_heuristic_value > heuristic_value:
                        closed.pop(closed_state.get_board_representation().get_board_str())
                        a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                        heapq.heappush(opened, a_star_node)
                        opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    continue
            else:
                # state is in open list
                previous_heuristic_value = opened_state.get_heuristic_value()
                # heuristic value is better that the old one
                if previous_heuristic_value > heuristic_value:
                    # replace the old node with a new one with the new heuristic value in the open list
                    opened.remove(opened_state)
                    opened_dictionary.pop(opened_state.get_state_representation().get_board_str())
                    heapq.heapify(opened)
                    a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                    heapq.heappush(opened, a_star_node)
                    opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    continue
        return

    @staticmethod
    def backwards(path):
        solution_backwards = path.split(" ")
        solution_backwards.reverse()
        solution = ""
        for sln_str in solution_backwards:
            if len(sln_str) < 3:
                continue
            if sln_str[1] == 'D':
                solution += sln_str[0] + "U" + sln_str[2]
            elif sln_str[1] == 'U':
                solution += sln_str[0] + "D" + sln_str[2]
            elif sln_str[1] == 'R':
                solution += sln_str[0] + "L" + sln_str[2]
            elif sln_str[1] == 'L':
                solution += sln_str[0] + "R" + sln_str[2]
            solution += " "
        return solution

    @staticmethod
    def reset():
        BiDirectionalAStar.opened_back_dictionary.clear()
        BiDirectionalAStar.opened_front_dictionary.clear()
        BiDirectionalAStar.opened_back.clear()
        BiDirectionalAStar.opened_front.clear()
        BiDirectionalAStar.closed_front.clear()
        BiDirectionalAStar.closed_back.clear()
