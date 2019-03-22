from rush_hour.Vehicle import Orientation


class TotalDistanceHeuristic:
    @staticmethod
    def calculate_heuristic_value(state, initial_state_vehicles):
        total_distance = 0

        for vehicle in initial_state_vehicles:
            state_vehicle = state.get_vehicle(vehicle.get_name())
            if vehicle.get_orientation() == Orientation.HORIZONTAL:
                total_distance += abs(state_vehicle.get_y_coordinate() - vehicle.get_y_coordinate())
            else:
                total_distance += abs(state_vehicle.get_x_coordinate() - vehicle.get_x_coordinate())
        return total_distance
