class BackwardsBlockingHeuristic:

    @staticmethod
    def calculate_heuristic_value(state):
        blocking_vehicles = []
        last_car = '\0'
        my_vehicle = state.get_vehicle('X')
        x_coordinate = my_vehicle.get_x_coordinate()
        y_coordinate = my_vehicle.get_y_coordinate()
        for i in range(state.get_board_size(),y_coordinate):
            if state.get_board()[x_coordinate][i] != 'X' and state.get_board()[x_coordinate][i] != '.':
                if state.get_board()[x_coordinate][i] == last_car:
                    raise Exception("State not valid")
                blocking_vehicles.append(state.get_board()[x_coordinate][i])
                last_car = state.get_board()[x_coordinate][i]
        return len(blocking_vehicles) + 1
        # return AdvancedBlockingHeuristic.calculate_heuristic_value(state) *-1


