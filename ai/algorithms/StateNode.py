class StateNode:
    def __init__(self, state_representation, heuristic_value, depth):
        self._state_representation = state_representation
        self._heuristic_value = heuristic_value
        self._depth = depth

    def get_state_representation(self):
        return self._state_representation

    def get_heuristic_value(self):
        return self._heuristic_value

    def get_depth(self):
        return self._depth

    def __lt__(self, other):
        if self._heuristic_value == other.get_heuristic_value():
            return len(self._state_representation.get_solution_path()) < len(other.get_state_representation().get_solution_path())
        return self._heuristic_value < other.get_heuristic_value()
