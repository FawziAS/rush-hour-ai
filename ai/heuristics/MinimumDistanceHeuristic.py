class MinimumDistanceHeuristic:
    @staticmethod
    def calculate_heuristic_value(state):
        my_vehicle = state.get_vehicle('X')
        y_coordinate = my_vehicle.get_y_coordinate()
        min_distance = state.get_board_size() - y_coordinate
        return min_distance / 6
