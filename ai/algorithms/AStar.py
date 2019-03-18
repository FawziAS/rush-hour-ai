import heapq
import time

import ai.heuristics

from ai.algorithms.StateNode import StateNode


class AStar:
    opened = []  # opened states list ( we implemented it as a heap so we can pop the best heuristic value state
    opened_dictionary = {}  # hash in order to find a state in open list faster
    closed = {}  # hash in order to find a state in closed faster
    # parameters for lab report investigations
    searched_nodes = 0
    nodes_num = 0
    min_depth = -1
    max_depth = 0
    sum_depth = 0
    sum_heuristic = 0
    win_depth = -1
    branching_factor = 0
    starting_timestamp = 0
    finishing_timestamp = 0

    @staticmethod
    def start_a_star(initial_state_representation, heuristic, time_limit, heuristic_limit=-1):
        # TODO: Change the return value from bool to Object or None (WinState)
        AStar.starting_timestamp = int(time.time())
        state = StateNode(initial_state_representation,
                          heuristic.calculate_heuristic_value(initial_state_representation), 1)
        AStar.min_depth = state.get_depth()
        heapq.heappush(AStar.opened, state)
        AStar.opened_dictionary.update({initial_state_representation.get_board_str(): state})
        previous_state = state
        curr_time = float(time.time()) - AStar.starting_timestamp
        # AStar keeps running until finding a solution or time limit exceeded
        while AStar.opened and curr_time < time_limit:
            state = heapq.heappop(AStar.opened)  # getting the best heuristic value state
            AStar.opened_dictionary.pop(state.get_state_representation().get_board_str())
            if state.get_depth() < previous_state.get_depth():
                if AStar.min_depth == -1:
                    AStar.min_depth = previous_state.get_depth()
                if previous_state.get_depth() < AStar.min_depth:
                    AStar.min_depth = previous_state.get_depth()
            AStar.searched_nodes += 1
            AStar.sum_depth += state.get_depth()
            AStar.sum_heuristic += state.get_heuristic_value()
            if state.get_depth() > AStar.max_depth:
                AStar.max_depth = state.get_depth()

            # algorithm found a winning state:
            if state.get_state_representation().win_state():
                AStar.finishing_timestamp = float(time.time())
                AStar.win_depth = state.get_depth()
                print(
                    "Solution: " + state.get_state_representation().get_solution_path() + state.get_state_representation().get_last_move())
                return True
            neighbor_states = state.get_state_representation().get_neighbours()
            # AStar.nodes_num += len(neighbor_states)
            AStar.add_relevant_states(neighbor_states, heuristic, state.get_depth(), heuristic_limit)
            AStar.closed.update({state.get_state_representation().get_board_str(): state})
            previous_state = state
            curr_time = float(time.time()) - AStar.starting_timestamp
        if curr_time > time_limit:
            print("FAILED")
        return False

    # adds the relevant states to the heap
    @staticmethod
    def add_relevant_states(neighbor_states, heuristic, previous_depth, heuristic_limit=-1):
        for state_representation in neighbor_states:
            heuristic_value = heuristic.calculate_heuristic_value(state_representation)
            if heuristic_limit != -1 and heuristic_value > heuristic_limit:
                continue
            opened_state = AStar.opened_dictionary.get(state_representation.get_board_str())
            # state is not in the open heap
            if opened_state is None:
                closed_state = AStar.closed.get(state_representation.get_board_str())
                # state wasn't visited before
                if closed_state is None:
                    # add it to the open heap
                    a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                    heapq.heappush(AStar.opened, a_star_node)
                    AStar.opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    AStar.nodes_num += 1
                    continue
                else:
                    # state is in closed list
                    previous_heuristic_value = closed_state.get_heuristic_value()
                    # if current heuristic value is better, delete the old node from closed and add the current to open
                    if previous_heuristic_value > heuristic_value:
                        AStar.closed.pop(closed_state.get_board_representation().get_board_str())
                        a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                        heapq.heappush(AStar.opened, a_star_node)
                        AStar.opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                        AStar.nodes_num += 1
                    continue
            else:
                # state is in open list
                previous_heuristic_value = opened_state.get_heuristic_value()
                # heuristic value is better that the old one
                if previous_heuristic_value > heuristic_value:
                    # replace the old node with a new one with the new heuristic value in the open list
                    AStar.opened.remove(opened_state)
                    AStar.opened_dictionary.pop(opened_state.get_state_representation().get_board_str())
                    heapq.heapify(AStar.opened)
                    a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                    heapq.heappush(AStar.opened, a_star_node)
                    AStar.opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    AStar.nodes_num += 1
                    continue
        return

    @staticmethod
    def get_game_info():
        info = ""
        info += "Solved in: " + str(AStar.finishing_timestamp - AStar.starting_timestamp) + " Seconds.\n"
        info += "SearchedNodes: " + str(AStar.searched_nodes) + "\n"
        info += "Penetrance: " + str(AStar.win_depth / AStar.searched_nodes) + "\n"
        info += "Avg. Heuristic: " + str(AStar.sum_heuristic / AStar.searched_nodes) + "\n"
        info += "EBF: " + str(AStar.nodes_num / AStar.searched_nodes) + "\n"
        info += "MinimumDepth: " + str(AStar.min_depth) + "\n"
        info += "MaxDepth: " + str(AStar.max_depth) + "\n"
        info += "Avg. Depth: " + str(AStar.sum_depth / AStar.searched_nodes) + "\n"
        return info

    @staticmethod
    def reset():
        AStar.opened.clear()
        AStar.closed.clear()
        AStar.searched_nodes = 0
        AStar.nodes_num = 0
        AStar.min_depth = -1
        AStar.max_depth = 0
        AStar.sum_depth = 0
        AStar.sum_heuristic = 0
        AStar.win_depth = -1
        AStar.branching_factor = 0
        AStar.starting_timestamp = 0
        AStar.finishing_timestamp = 0
