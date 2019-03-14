import heapq


class AStar:
    opened = []
    opened_dictionary = {}
    closed = {}

    @staticmethod
    def start_a_star(initial_state, heuristic):
        heapq.heappush(AStar.opened, initial_state)
        AStar.opened_dictionary.update({initial_state.get_board_str(): initial_state})
        while AStar.opened:
            state = heapq.heappop(AStar.opened)
            AStar.opened_dictionary.pop(state.get_board_str())
            if state.win_state():
                print("Solution: " + state.get_solution_path() + state.get_last_move())
                break
            neighbor_states = state.get_neighbours()
            AStar.add_relevant_states(neighbor_states, heuristic)
            AStar.closed.update({state.get_board_str(): state})

    @staticmethod
    def add_relevant_states(neighbor_states, heuristic):
        for state in neighbor_states:
            heuristic_value = heuristic.calculate_heuristic_value(state)
            previous_state = AStar.opened_dictionary.get(state.get_board_str())
            if previous_state is None:
                previous_state = AStar.closed.get(state.get_board_str())
                if previous_state is None:
                    heapq.heappush(AStar.opened, state)
                    AStar.opened_dictionary.update({state.get_board_str(): state})
                    continue
                else:
                    previous_heuristic_value = previous_state.get_heuristic_value()
                    if previous_heuristic_value > heuristic_value:
                        AStar.closed.pop(previous_state.get_board_str())
                        heapq.heappush(AStar.opened, state)
                        AStar.opened_dictionary.update({state.get_board_str(): state})
                    continue
            else:
                previous_heuristic_value = previous_state.get_heuristic_value()
                if previous_heuristic_value > heuristic_value:
                    AStar.opened.remove(previous_state)
                    AStar.opened_dictionary.pop(previous_state.get_board_str())
                    heapq.heapify(AStar.opened)
                    heapq.heappush(AStar.opened, state)
                    AStar.opened_dictionary.update({state.get_board_str(): state})
                    continue
        return

    @staticmethod
    def reset():
        AStar.opened.clear()
        AStar.closed.clear()
