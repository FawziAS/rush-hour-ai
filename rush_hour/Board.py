from enum import Enum
from rush_hour.Vehicle import Vehicle, Orientation


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Board:
    def __init__(self, initial_state):
        self._board_size = 6
        self._board = []
        for i in range(self._board_size):
            self._board.append(self._board_size * ['.'])
        self.parse_board(initial_state)
        self._vehicles_on_board = []
        self._vehicles_on_board_dictionary = {}
        self.set_vehicles_from_board()
        self._solution_path = ""

    def parse_board(self, initial_state):
        s = 0
        for i in range(0, self._board_size):
            for j in range(0, self._board_size):
                self._board[i][j] = initial_state[s]
                s += 1

    def set_vehicles_from_board(self):
        for i in range(0, self._board_size):
            for j in range(0, self._board_size):
                if self.check_board_contains(self._board[i][j]):
                    continue
                elif self._board[i][j] == '.':
                    continue
                vehicle = self.get_car(i, j)
                self._vehicles_on_board.append(vehicle)
                self._vehicles_on_board_dictionary.update({vehicle.get_name(): vehicle})

    def set_solution_path(self, path):
        self._solution_path += path

    def get_solution_path(self):
        return self._solution_path

    def get_last_move(self):
        my_vehicle = self.get_vehicle("X")
        return "XR" + str(self._board_size - my_vehicle.get_y_coordinate())

    def check_board_contains(self, vehicle_name):
        vehicle = self._vehicles_on_board_dictionary.get(vehicle_name)
        if vehicle is None:
            return False
        return True

    def get_vehicles_on_board(self):
        return self._vehicles_on_board

    def get_car(self, i, j):
        vehicle_name = self._board[i][j]
        # In case the vehicle size is 3
        if i + 2 < self._board_size:
            if vehicle_name == self._board[i + 2][j]:
                return Vehicle(3, vehicle_name, Orientation.VERTICAL, i, j)
        if j + 2 < self._board_size:
            if vehicle_name == self._board[i][j + 2]:
                return Vehicle(3, vehicle_name, Orientation.HORIZONTAL, i, j)
        if i + 1 < self._board_size:
            if vehicle_name == self._board[i + 1][j]:
                return Vehicle(2, vehicle_name, Orientation.VERTICAL, i, j)
        if j + 1 < self._board_size:
            if vehicle_name == self._board[i][j + 1]:
                return Vehicle(2, vehicle_name, Orientation.HORIZONTAL, i, j)

    def get_board_size(self):
        return self._board_size

    def board_to_string(self):
        board_string = "    1 2 3 4 5 6\n"
        board_string += "  +-------------+\n"
        for i in range(self._board_size):
            board_string += str(i + 1) + " | "
            for j in range(self._board_size):
                board_string += self._board[i][j] + " "
            if i == 2:
                board_string += "  ==>\n"
            else:
                board_string += "|\n"
        board_string += "  +-------------+\n"
        board_string += "    a b c d e f\n"
        return board_string

    def print_board(self):
        print(self.board_to_string())

    def get_board(self):
        return self._board

    def move_vehicle_on_board(self, vehicle_name, move_direction, steps_on_board):
        vehicle = self.get_vehicle(vehicle_name)
        if vehicle is None:
            return False
        x = vehicle.get_x_coordinate()
        y = vehicle.get_y_coordinate()
        if self.check_move(vehicle, move_direction, steps_on_board):
            if vehicle.get_orientation() == Orientation.VERTICAL:
                for i in range(vehicle.get_size()):
                    self._board[x][y] = '.'
                    x += 1
                for i in range(vehicle.get_size()):
                    self._board[vehicle.get_x_coordinate() + i][y] = vehicle_name
                return True

            if vehicle.get_orientation() == Orientation.HORIZONTAL:
                for i in range(vehicle.get_size()):
                    self._board[x][y] = '.'
                    y += 1
                for i in range(vehicle.get_size()):
                    self._board[x][vehicle.get_y_coordinate() + i] = vehicle_name
                return True
        return False

    def get_vehicle(self, vehicle_name):
        vehicle = self._vehicles_on_board_dictionary.get(vehicle_name)
        if vehicle is not None:
            return vehicle
        return None

    # checking the move(direction and steps number) if it's valid, if it is valid, we move the vehicle on the board, if not we don't change the board
    def check_move(self, vehicle, move_direction, steps_on_board):
        if vehicle.get_orientation() == Orientation.HORIZONTAL and (
                move_direction == Direction.DOWN or move_direction == Direction.UP):
            return False
        if vehicle.get_orientation() == Orientation.VERTICAL and (
                move_direction == Direction.LEFT or move_direction == Direction.RIGHT):
            return False
        if move_direction == Direction.UP:
            i = 1
            while i <= steps_on_board:
                if vehicle.get_x_coordinate() - i < 0:
                    return False
                if self._board[vehicle.get_x_coordinate() - i][vehicle.get_y_coordinate()] != '.':
                    return False
                i += 1
            vehicle.move_vehicle(vehicle.get_x_coordinate() - steps_on_board, vehicle.get_y_coordinate())
            return True
        if move_direction == Direction.DOWN:
            i = 1
            place = vehicle.get_x_coordinate() + vehicle.get_size() - 1
            while i <= steps_on_board:
                if place + i >= self._board_size:
                    return False
                if self._board[place + i][vehicle.get_y_coordinate()] != '.':
                    return False
                i += 1
            vehicle.move_vehicle(vehicle.get_x_coordinate() + steps_on_board, vehicle.get_y_coordinate())
            return True
        if move_direction == Direction.LEFT:
            i = 1
            while i <= steps_on_board:
                if vehicle.get_y_coordinate() - i < 0:
                    return False
                if self._board[vehicle.get_x_coordinate()][vehicle.get_y_coordinate() - i] != '.':
                    return False
                i += 1
            vehicle.move_vehicle(vehicle.get_x_coordinate(), vehicle.get_y_coordinate() - steps_on_board)
            return True
        if move_direction == Direction.RIGHT:
            place = vehicle.get_y_coordinate() + vehicle.get_size() - 1
            i = 1
            while i <= steps_on_board:
                if place + i >= self._board_size:
                    return False
                if self._board[vehicle.get_x_coordinate()][i + place] != '.':
                    return False
                i += 1
            vehicle.move_vehicle(vehicle.get_x_coordinate(), vehicle.get_y_coordinate() + steps_on_board)
            return True
        return False

    # checking if the current board is a win state
    def win_state(self):
        my_vehicle = self.get_vehicle('X')
        x = my_vehicle.get_x_coordinate()
        y = my_vehicle.get_y_coordinate()
        if x != 2:
            return False
        else:
            while y < self._board_size:
                if self._board[x][y] != '.' and self._board[x][y] != 'X':
                    return False
                y += 1
            return True

    # getting all the neighbor boards from current board, we create them by doing all the possible moves
    def get_neighbours(self):
        neighbours = []
        for vehicle in self._vehicles_on_board:
            if vehicle.get_orientation() == Orientation.HORIZONTAL:
                # right move
                for i in range(1, 5):
                    success = self.move_vehicle_on_board(vehicle.get_name(), Direction.RIGHT, i)
                    if success:
                        neighbour_board = Board(self.get_board_str())
                        self.move_vehicle_on_board(vehicle.get_name(), Direction.LEFT, i)
                        neighbour_board.set_solution_path(
                            self.get_solution_path() + vehicle.get_name() + "R" + str(i) + " ")
                        neighbours.append(neighbour_board)
                    else:
                        break
                # left move
                for i in range(1, 5):
                    success = self.move_vehicle_on_board(vehicle.get_name(), Direction.LEFT, i)
                    if success:
                        neighbour_board = Board(self.get_board_str())
                        self.move_vehicle_on_board(vehicle.get_name(), Direction.RIGHT, i)
                        neighbour_board.set_solution_path(
                            self.get_solution_path() + vehicle.get_name() + "L" + str(i) + " ")
                        neighbours.append(neighbour_board)
                    else:
                        break

            if vehicle.get_orientation() == Orientation.VERTICAL:
                # up move
                for i in range(1, 5):
                    success = self.move_vehicle_on_board(vehicle.get_name(), Direction.UP, i)
                    if success:
                        neighbour_board = Board(self.get_board_str())
                        self.move_vehicle_on_board(vehicle.get_name(), Direction.DOWN, i)
                        neighbour_board.set_solution_path(
                            self.get_solution_path() + vehicle.get_name() + "U" + str(i) + " ")
                        neighbours.append(neighbour_board)
                    else:
                        break
                # down move
                for i in range(1, 5):
                    success = self.move_vehicle_on_board(vehicle.get_name(), Direction.DOWN, i)
                    if success:
                        neighbour_board = Board(self.get_board_str())
                        self.move_vehicle_on_board(vehicle.get_name(), Direction.UP, i)
                        neighbour_board.set_solution_path(
                            self.get_solution_path() + vehicle.get_name() + "D" + str(i) + " ")
                        neighbours.append(neighbour_board)
                    else:
                        break
        return neighbours

    def get_board_str(self):
        board_str = ""
        for i in range(self._board_size):
            for j in range(self._board_size):
                board_str += self._board[i][j]
        return board_str

    def get_blocking_vehicles(self):
        blocking_vehicles = []
        last_car = '\0'
        my_vehicle = self.get_vehicle('X')
        x_coordinate = my_vehicle.get_x_coordinate()
        y_coordinate = my_vehicle.get_y_coordinate()
        for i in range(y_coordinate, self.get_board_size()):
            if self.get_board()[x_coordinate][i] != 'X' and self.get_board()[x_coordinate][i] != '.':
                if self.get_board()[x_coordinate][i] == last_car:
                    raise Exception("State not valid")
                blocking_vehicles.append(self.get_board()[x_coordinate][i])
                last_car = self.get_board()[x_coordinate][i]
        return blocking_vehicles

    def get_vehicle_theoretical_place(self,vehicle):
        my_vehicle_x = self.get_vehicle('X').get_x_coordinate()
        up_moves = vehicle.get_size() - (my_vehicle_x - vehicle.get_x_coordinate())
        down_moves = vehicle.get_size() - up_moves + 1
        if vehicle.get_x_coordinate() - up_moves < 0:
            return vehicle.get_x_coordinate() + down_moves
        elif vehicle.get_x_coordinate() + vehicle.get_size() + down_moves >= self.get_board_size():
            return vehicle.get_x_coordinate() - up_moves
        elif up_moves > down_moves:
            return vehicle.get_x_coordinate() + down_moves
        else:
            return vehicle.get_x_coordinate() - up_moves
