import math


class UnblockingHeuristic:
    @staticmethod
    def calculate_heuristic_value(state):
        # blocking_vehicles = state.get_blocking_vehicles()
        # heuristic_value = 0
        # my_vehicle_x = state.get_vehicle('X').get_x_coordinate()
        # for vehicle_name in blocking_vehicles:
        #     vehicle = state.get_vehicle(vehicle_name)
        #     up_moves = vehicle.get_size() - (my_vehicle_x - vehicle.get_x_coordinate())
        #     down_moves = vehicle.get_size() - up_moves + 1
        #     if vehicle.get_x_coordinate() - up_moves < 0:
        #         heuristic_value += down_moves
        #         continue
        #     elif vehicle.get_x_coordinate() + vehicle.get_size() + down_moves >= state.get_board_size():
        #         heuristic_value += up_moves
        #         continue
        #     elif up_moves > down_moves:
        #         heuristic_value += down_moves
        #         continue
        #     else:
        #         heuristic_value += up_moves
        # return heuristic_value

        blocking_vehicles = state.get_blocking_vehicles()
        heuristic_value = 0
        for vehicle_name in blocking_vehicles:
            my_vehicle = state.get_vehicle(vehicle_name)
            heuristic_value = heuristic_value + math.fabs(state.get_vehicle_theoretical_place(my_vehicle) - my_vehicle.get_x_coordinate())
        return heuristic_value

