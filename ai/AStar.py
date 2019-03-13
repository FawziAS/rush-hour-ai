import heapq

from ai.BlockingHeuristic import BlockingHeuristic


class AStar:
    opened = []
    closed = []

    @staticmethod
    def start_a_star(initial_state, heuristic):
        heuristic_value = heuristic.calculate_heuristic_value(initial_state)
        heapq.heappush(AStar.opened, initial_state)
        while AStar.opened:
            state = heapq.heappop(AStar.opened)
            if state.win_state():
                print("Solution: " + state.get_solution_path() + state.get_last_move())
                break
            neighbor_states = state.get_neighbours()
            AStar.add_relevant_states(neighbor_states, heuristic)
            AStar.closed.append(state)

    @staticmethod
    def add_relevant_states(neighbor_states, heuristic):
        for state in neighbor_states:
            heuristic_value = heuristic.calculate_heuristic_value(state)
            previous_state = AStar.a_star_contains(state, AStar.opened)
            if previous_state is None:
                previous_state = AStar.a_star_contains(state, AStar.closed)
                if previous_state is None:
                    heapq.heappush(AStar.opened, state)
                    continue
                else:
                    previous_heuristic_value = previous_state.get_heuristic_value()
                    if previous_heuristic_value > heuristic_value:
                        AStar.closed.remove(previous_state)
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
    def a_star_contains(state, given_list):
        for prev_state in given_list:
            if prev_state.get_board() == state.get_board():
                return prev_state
        return None
