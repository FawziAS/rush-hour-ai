from rush_hour.Board import Board


class AdvancedBlockingHeuristic:
    @staticmethod
    def calculate_heuristic_value(state):
        blocking_vehicles = state.get_blocking_vehicles()
        heuristic_value = 1 + len(blocking_vehicles)
        for vehicle_name in blocking_vehicles:
            my_vehicle = state.get_vehicle(vehicle_name)
            theoretical_x = state.get_vehicle_theoretical_place(my_vehicle)
            heuristic_value += AdvancedBlockingHeuristic.num_blocking_cars(my_vehicle, theoretical_x, state)
        return heuristic_value

    @staticmethod
    def num_blocking_cars(my_vehicle, theoretical_x, state):
        blocking_number = 0
        checked_vehicles = {}
        x_coordinate = my_vehicle.get_x_coordinate()
        y_coordinate = my_vehicle.get_y_coordinate()
        state_board = state.get_board()
        if x_coordinate > theoretical_x:
            for i in range(x_coordinate, theoretical_x, -1):
                if state_board[i][y_coordinate] != my_vehicle.get_name() and state_board[i][y_coordinate] != '.':
                    exists = checked_vehicles.get(state_board[i][y_coordinate])
                    if exists is not None:
                        continue
                    else:
                        checked_vehicles.update({state_board[i][y_coordinate]: True})
                        blocking_number += 1
            return blocking_number
        else:
            for i in range(x_coordinate, theoretical_x+my_vehicle.get_size()):
                if state_board[i][y_coordinate] != my_vehicle.get_name() and state_board[i][y_coordinate] != '.':
                    exists = checked_vehicles.get(state_board[i][y_coordinate])
                    if exists is not None:
                        continue
                    else:
                        checked_vehicles.update({state_board[i][y_coordinate]: True})
                        blocking_number += 1
            return blocking_number
