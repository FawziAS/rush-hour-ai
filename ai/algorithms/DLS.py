from rush_hour.Board import Board

# Depth limited search
class DLS:
    states_stack = []
    closed = {}

    @staticmethod
    def start_dls(initial_state, limit=1):
        DLS.states_stack.append((0, initial_state))
        while DLS.states_stack:
            current_state = DLS.states_stack.pop()
            if current_state[1].win_state():
                return current_state[1]
            if current_state[0] == limit:
                DLS.closed.update({current_state[1].get_board_str(): current_state})
                continue
            neighbours = current_state[1].get_neighbours()
            while neighbours:
                upcoming_state = neighbours.pop()
                if upcoming_state.get_board_str() not in DLS.closed:
                    DLS.states_stack.append((current_state[0] + 1, upcoming_state))
                    DLS.closed.update({upcoming_state.get_board_str(): upcoming_state})
                    break
        return None

    @staticmethod
    def add_relevant_nodes(nodes_list, parent_depth):
        for node in nodes_list:
            DLS.states_stack.append((parent_depth, node))

    @staticmethod
    def reset_stack():
        DLS.states_stack.clear()
