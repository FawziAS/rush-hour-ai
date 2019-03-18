from rush_hour.Board import Board


class BlockingBlockingHeuristic:
    @staticmethod
    def calculate_heuristic_value(state):
        blocking_vehicles = state.get_blocking_vehicles()
        heuristic_value = 0
        for vehicle_name in blocking_vehicles:
            my_vehicle = state.get_vehicle(vehicle_name)
            theoretical_x = state.get_vehicle_theoretical_place(my_vehicle)
            heuristic_value += BlockingBlockingHeuristic.num_blocking_cars(my_vehicle, theoretical_x, state)
        return heuristic_value

    @staticmethod
    def num_blocking_cars(my_vehicle, theoretical_x, state):
        blocking_number = 0
        checked_vehicles = {}
        x_coordinate = my_vehicle.get_x_coordinate()
        y_coordinate = my_vehicle.get_y_coordinate()
        if x_coordinate > theoretical_x:
            for i in range(x_coordinate, theoretical_x, -1):
                if state.get_board()[i][y_coordinate] != my_vehicle.get_name() and state.get_board()[i][
                    y_coordinate] != '.':
                    if checked_vehicles.get(state.get_board()[i][y_coordinate]):
                        continue
                    else:
                        checked_vehicles.update(state.get_board()[i][y_coordinate])
                        blocking_number += 1
            return blocking_number
        else:
            for i in range(x_coordinate, theoretical_x):
                if state.get_board()[i][y_coordinate] != my_vehicle.get_name() and state.get_board()[i][
                    y_coordinate] != '.':
                    if checked_vehicles.get(state.get_board()[i][y_coordinate]):
                        continue
                    else:
                        checked_vehicles.update(state.get_board()[i][y_coordinate])
                        blocking_number += 1
            return blocking_number
