import heapq
import time

import ai.heuristics

from ai.algorithms.StateNode import StateNode


class AStar:
    opened = []
    opened_dictionary = {}
    closed = {}
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
    def start_a_star(initial_state_representation, heuristic, time_limit):
        AStar.starting_timestamp = int(time.time())
        state = StateNode(initial_state_representation,
                          heuristic.calculate_heuristic_value(initial_state_representation), 1)
        AStar.min_depth = state.get_depth()
        heapq.heappush(AStar.opened, state)
        AStar.opened_dictionary.update({initial_state_representation.get_board_str(): state})
        previous_state = state
        curr_time = float(time.time()) - AStar.starting_timestamp
        while AStar.opened and curr_time < time_limit:
            state = heapq.heappop(AStar.opened)
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
            if state.get_state_representation().win_state():
                AStar.finishing_timestamp = float(time.time())
                AStar.win_depth = state.get_depth()
                print(
                    "Solution: " + state.get_state_representation().get_solution_path() + state.get_state_representation().get_last_move())
                break
            neighbor_states = state.get_state_representation().get_neighbours()
            # AStar.nodes_num += len(neighbor_states)
            AStar.add_relevant_states(neighbor_states, heuristic, state.get_depth())
            AStar.closed.update({state.get_state_representation().get_board_str(): state})
            previous_state = state
            curr_time = float(time.time()) - AStar.starting_timestamp
        if curr_time > time_limit:
            print("FAILED")

    @staticmethod
    def add_relevant_states(neighbor_states, heuristic, previous_depth):
        for state_representation in neighbor_states:
            heuristic_value = heuristic.calculate_heuristic_value(state_representation)
            opened_state = AStar.opened_dictionary.get(state_representation.get_board_str())
            if opened_state is None:
                closed_state = AStar.closed.get(state_representation.get_board_str())
                if closed_state is None:
                    a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                    heapq.heappush(AStar.opened, a_star_node)
                    AStar.opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                    AStar.nodes_num += 1
                    continue
                else:
                    previous_heuristic_value = closed_state.get_heuristic_value()
                    if previous_heuristic_value > heuristic_value:
                        AStar.closed.pop(closed_state.get_board_representation().get_board_str())
                        a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                        heapq.heappush(AStar.opened, a_star_node)
                        AStar.opened_dictionary.update({state_representation.get_board_str(): a_star_node})
                        AStar.nodes_num += 1
                    continue
            else:
                previous_heuristic_value = opened_state.get_heuristic_value()
                if previous_heuristic_value > heuristic_value:
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
        info += "Effective BF: " + "\n"
        # info += "Avg. BranchingFactor: " + str(AStar.nodes_num / AStar.searched_nodes) + "\n"
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
