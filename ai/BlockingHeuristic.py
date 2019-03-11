from rush_hour import Board, Vehicle


class BlockingHeuristic:
    @staticmethod
    def calculate_heuristic_value(state):
        blocking_vehicles = 1
        last_car = '\0'
        my_vehicle = state.get_vehicle('X')
        x_coordinate = my_vehicle.get_x_coordinate()
        y_coordinate = my_vehicle.get_y_coordinate()
        for i in range(y_coordinate, state.get_board_size()):
            if state[x_coordinate][i] != 'X' and state[x_coordinate][i] != '.':
                if state[x_coordinate][i] != last_car:
                    raise Exception("State not valid")
                blocking_vehicles += 1
                last_car = state[x_coordinate][i]
        return blocking_vehicles
