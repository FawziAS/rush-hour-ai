import math


class UnblockingHeuristic:
    @staticmethod
    def calculate_heuristic_value(state):
        blocking_vehicles = state.get_blocking_vehicles()
        heuristic_value = 0
        for vehicle_name in blocking_vehicles:
            my_vehicle = state.get_vehicle(vehicle_name)
            heuristic_value = heuristic_value + math.fabs(state.get_vehicle_theoretical_place(my_vehicle) - my_vehicle.get_x_coordinate())
        return heuristic_value

