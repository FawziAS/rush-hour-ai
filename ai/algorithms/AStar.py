import heapq


class AStar:
    opened = []
    closed = {}

    @staticmethod
    def start_a_star(initial_state, heuristic):
        heapq.heappush(AStar.opened, initial_state)
        while AStar.opened:
            state = heapq.heappop(AStar.opened)
            if state.win_state():
                print("Solution: " + state.get_solution_path() + state.get_last_move())
                break
            neighbor_states = state.get_neighbours()
            AStar.add_relevant_states(neighbor_states, heuristic)
            AStar.closed.update({state.get_board_str():state})

    @staticmethod
    def add_relevant_states(neighbor_states, heuristic):
        for state in neighbor_states:
            heuristic_value = heuristic.calculate_heuristic_value(state)
            previous_state = AStar.a_star_opened_contains(state, AStar.opened)
            if previous_state is None:
                previous_state = AStar.closed.get(state.get_board_str())
                if previous_state is None:
                    heapq.heappush(AStar.opened, state)
                    continue
                else:
                    previous_heuristic_value = previous_state.get_heuristic_value()
                    if previous_heuristic_value > heuristic_value:
                        AStar.closed.pop(previous_state.get_board_str())
                        heapq.heappush(AStar.opened, state)
                    continue
            else:
                previous_heuristic_value = previous_state.get_heuristic_value()
                if previous_heuristic_value > heuristic_value:
                    AStar.opened.remove(previous_state)
                    heapq.heapify(AStar.opened)
                    heapq.heappush(AStar.opened, state)
                    continue
        return

    @staticmethod
    def a_star_opened_contains(state, given_list):
        current_board = state.get_board()
        for prev_state in given_list:
            if prev_state.get_board() == current_board:
                return prev_state
        return None

    @staticmethod
    def reset():
        AStar.opened.clear()
        AStar.closed.clear()
