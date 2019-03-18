from rush_hour import Board, Vehicle


# A heuristic that calculates the number of cars blocking the X car + 1
class BlockingHeuristic:
    @staticmethod
    def calculate_heuristic_value(state):
        blocking_vehicles = state.get_blocking_vehicles()
        return 1 + len(blocking_vehicles)
