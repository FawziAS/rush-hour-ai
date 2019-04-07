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
    sum_depth = 0
    nodes_num = 0
    sum_heuristic = 0
    win_depth = 0
    searched_nodes = 0
    opened_front = []
    opened_front_dictionary = {}
    opened_back = []
    opened_back_dictionary = {}
    closed_front = {}
    closed_back = {}
    starting_timestamp = 0
    finishing_timestamp = 0

    @staticmethod
    def start_bidirectional_a_star(initial_state_representation, goal_state_representation, heuristic, time_limit):
        BiDirectionalAStar.reset()
        BiDirectionalAStar.starting_timestamp = float(time.time())
        initial_state = StateNode(initial_state_representation,
                                  heuristic.calculate_heuristic_value(initial_state_representation), 0)
        BiDirectionalAStar.initial_state_rep = initial_state_representation
        vehicles_on_initial_board = initial_state_representation.get_vehicles_on_board()
        goal_state_representation.set_solution_path(
            BiDirectionalAStar.backwards(goal_state_representation.get_last_move()))
        goal_state = StateNode(goal_state_representation,
                               0, 0)

        # Added initial states
        heapq.heappush(BiDirectionalAStar.opened_front, initial_state)
        BiDirectionalAStar.opened_front_dictionary.update({initial_state_representation.get_board_str(): initial_state})
        heapq.heappush(BiDirectionalAStar.opened_back, goal_state)
        BiDirectionalAStar.opened_back_dictionary.update({goal_state_representation.get_board_str(): goal_state})
        curr_time = time.time() - BiDirectionalAStar.starting_timestamp
        while BiDirectionalAStar.opened_front and BiDirectionalAStar.opened_back and curr_time < time_limit:
            # Get the heuristically best state from the first AStar and try to match it form the second AStar.
            front_state = heapq.heappop(BiDirectionalAStar.opened_front)
            BiDirectionalAStar.opened_front_dictionary.pop(front_state.get_state_representation().get_board_str())
            BiDirectionalAStar.closed_front.update(
                {front_state.get_state_representation().get_board_str(): front_state})
            # For analysis purposes.
            BiDirectionalAStar.searched_nodes += 1
            BiDirectionalAStar.sum_depth += front_state.get_depth()
            BiDirectionalAStar.sum_heuristic += front_state.get_heuristic_value()

            match_found = BiDirectionalAStar.connection_exists(front_state, Direction.FORWARD)
            if match_found is not None:
                BiDirectionalAStar.finishing_timestamp = float(time.time())
                backwards_path = BiDirectionalAStar.backwards(
                    match_found.get_state_representation().get_solution_path())
                BiDirectionalAStar.win_depth = front_state.get_depth() + match_found.get_depth()
                print("Solution: " + front_state.get_state_representation().get_solution_path() + backwards_path)
                print(BiDirectionalAStar.get_game_info())
                return
            # Get the heuristically best state from the second AStar and try to match it form the first AStar.
            back_state = heapq.heappop(BiDirectionalAStar.opened_back)
            BiDirectionalAStar.opened_back_dictionary.pop(back_state.get_state_representation().get_board_str())
            BiDirectionalAStar.closed_back.update({back_state.get_state_representation().get_board_str(): back_state})

            BiDirectionalAStar.searched_nodes += 1
            BiDirectionalAStar.sum_depth += back_state.get_depth()
            BiDirectionalAStar.sum_heuristic += back_state.get_heuristic_value()

            match_found = BiDirectionalAStar.connection_exists(back_state, Direction.BACKWARD)
            if match_found is not None:
                BiDirectionalAStar.finishing_timestamp = float(time.time())
                backwards_path = BiDirectionalAStar.backwards(back_state.get_state_representation().get_solution_path())
                BiDirectionalAStar.win_depth = back_state.get_depth() + match_found.get_depth()
                print("Solution: " + match_found.get_state_representation().get_solution_path() + backwards_path)
                print(BiDirectionalAStar.get_game_info())
                return

            # If no match has been found expand the best nodes (heuristically) from both sides.
            front_neighbours = front_state.get_state_representation().get_neighbours()
            back_neighbours = back_state.get_state_representation().get_neighbours()

            BiDirectionalAStar.add_forward_relevant_states(front_neighbours, BiDirectionalAStar.opened_front,
                                                           BiDirectionalAStar.opened_front_dictionary,
                                                           BiDirectionalAStar.closed_front, heuristic,
                                                           front_state.get_depth())

            BiDirectionalAStar.add_backwards_relevant_states(back_neighbours, BiDirectionalAStar.opened_back,
                                                             BiDirectionalAStar.opened_back_dictionary,
                                                             BiDirectionalAStar.closed_back, heuristic,
                                                             goal_state_representation,
                                                             back_state.get_depth())
            curr_time = time.time() - BiDirectionalAStar.starting_timestamp
        print("Failed")
        return

    @staticmethod
    def connection_exists(state, search_direction):
        # Checks if a there is a connection.
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
                    BiDirectionalAStar.nodes_num += 1
                    continue
                else:
                    # state is in closed list
                    previous_heuristic_value = closed_state.get_heuristic_value()
                    # if current heuristic value is better, delete the old node from closed and add the current to open
                    if previous_heuristic_value > heuristic_value:
                        closed.pop(closed_state.get_state_representation().get_board_str())
                        a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                        heapq.heappush(opened, a_star_node)
                        opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                        BiDirectionalAStar.nodes_num += 1
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
                    BiDirectionalAStar.nodes_num += 1
                    continue
        return

    @staticmethod
    def add_backwards_relevant_states(neighbour_states, opened, opened_dictionary, closed, heuristic, goal_state,
                                      previous_depth):
        for state_representation in neighbour_states:
            heuristic_value = heuristic.calculate_heuristic_value(goal_state) - heuristic.calculate_heuristic_value(
                state_representation)
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
                    BiDirectionalAStar.nodes_num += 1
                    continue
                else:
                    # state is in closed list
                    previous_heuristic_value = closed_state.get_heuristic_value()
                    # if current heuristic value is better, delete the old node from closed and add the current to open
                    if previous_heuristic_value > heuristic_value:
                        closed.pop(closed_state.get_state_representation().get_board_str())
                        a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                        heapq.heappush(opened, a_star_node)
                        opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                        BiDirectionalAStar.nodes_num += 1
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
                    BiDirectionalAStar.nodes_num += 1
                    continue
        return

    @staticmethod
    def backwards(path):
        # Reverse the solution path for the second AStar.
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
    def get_game_info():
        info = ""
        info += "Solved in: " + str(
            BiDirectionalAStar.finishing_timestamp - BiDirectionalAStar.starting_timestamp) + " Seconds.\n"
        info += "SearchedNodes: " + str(BiDirectionalAStar.searched_nodes) + "\n"
        info += "Penetrance: " + str(BiDirectionalAStar.win_depth / BiDirectionalAStar.searched_nodes) + "\n"
        info += "Avg. Heuristic: " + str(BiDirectionalAStar.sum_heuristic / BiDirectionalAStar.searched_nodes) + "\n"
        info += "EBF: " + str(BiDirectionalAStar.nodes_num / BiDirectionalAStar.searched_nodes) + "\n"
        info += "Avg. Depth: " + str(BiDirectionalAStar.sum_depth / BiDirectionalAStar.searched_nodes) + "\n"
        return info

    @staticmethod
    def reset():
        # Reset Bidirectional AStar.
        BiDirectionalAStar.opened_back_dictionary.clear()
        BiDirectionalAStar.opened_front_dictionary.clear()
        BiDirectionalAStar.opened_back.clear()
        BiDirectionalAStar.opened_front.clear()
        BiDirectionalAStar.closed_front.clear()
        BiDirectionalAStar.closed_back.clear()
        BiDirectionalAStar.sum_depth = 0
        BiDirectionalAStar.nodes_num = 0
        BiDirectionalAStar.sum_heuristic = 0
        BiDirectionalAStar.win_depth = 0
        BiDirectionalAStar.searched_nodes = 0
        BiDirectionalAStar.starting_timestamp = 0
        BiDirectionalAStar.finishing_timestamp = 0
