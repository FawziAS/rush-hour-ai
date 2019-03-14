import heapq
import ai.heuristics

from ai.algorithms.StateNode import StateNode


class AStar:
    opened = []
    opened_dictionary = {}
    closed = {}

    @staticmethod
    def start_a_star(initial_state_representation, heuristic):
        searched_nodes = 0
        state = StateNode(initial_state_representation,
                          heuristic.calculate_heuristic_value(initial_state_representation), 1)
        heapq.heappush(AStar.opened, state)
        AStar.opened_dictionary.update({initial_state_representation.get_board_str(): state})
        while AStar.opened:
            searched_nodes += 1
            state = heapq.heappop(AStar.opened)
            AStar.opened_dictionary.pop(state.get_state_representation().get_board_str())
            if state.get_state_representation().win_state():
                print(
                    "Solution: " + state.get_state_representation().get_solution_path() + state.get_state_representation().get_last_move())
                break
            neighbor_states = state.get_state_representation().get_neighbours()
            AStar.add_relevant_states(neighbor_states, heuristic, state.get_depth())
            AStar.closed.update({state.get_state_representation().get_board_str(): state})

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
                    continue
                else:
                    previous_heuristic_value = closed_state.get_heuristic_value()
                    if previous_heuristic_value > heuristic_value:
                        AStar.closed.pop(closed_state.get_board_representation().get_board_str())
                        a_star_node = StateNode(state_representation, heuristic_value, previous_depth + 1)
                        heapq.heappush(AStar.opened, a_star_node)
                        AStar.opened_dictionary.update({state_representation.get_board_str(): a_star_node})
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
                    continue
        return

    @staticmethod
    def reset():
        AStar.opened.clear()
        AStar.closed.clear()
