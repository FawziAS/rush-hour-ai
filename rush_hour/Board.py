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
        self.set_vehicles_from_board()

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
                self._vehicles_on_board.append(self.get_car(i, j))

    def check_board_contains(self, vehicle_name):
        for vehicle in self._vehicles_on_board:
            if vehicle.get_name() == vehicle_name:
                return True
        return False

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

    def move_vehicle_on_board(self, vehicle_name, move_direction, steps_on_board):
        vehicle = self.get_vehicle(vehicle_name)
        if vehicle is None:
            return False
        x = vehicle._x_coordinate
        y = vehicle._y_coordinate
        if self.check_move(vehicle, move_direction, steps_on_board):
            if vehicle.get_orientation() == Orientation.VERTICAL:
                for i in range(vehicle._size):
                    self._board[x][y] = '.'
                    x += 1
                for i in range(vehicle._size):
                    self._board[vehicle._x_coordinate + i][y] = vehicle_name
                return True

            if vehicle.get_orientation() == Orientation.HORIZONTAL:
                for i in range(vehicle._size):
                    self._board[x][y] = '.'
                    y += 1
                for i in range(vehicle._size):
                    self._board[x][vehicle._y_coordinate + i] = vehicle_name
                return True
        return False

    def get_vehicle(self, vehicle_name):
        for vehicle in self._vehicles_on_board:
            if vehicle.get_name() == vehicle_name:
                return vehicle
        return None

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
                if vehicle._x_coordinate - i < 0:
                    return False
                if self._board[vehicle._x_coordinate - i][vehicle._y_coordinate] != '.':
                    return False
                i += 1
            vehicle.move_vehicle(vehicle._x_coordinate - steps_on_board, vehicle._y_coordinate)
            return True
        if move_direction == Direction.DOWN:
            i = 1
            place = vehicle._x_coordinate + vehicle._size - 1
            while i <= steps_on_board:
                if place + i >= self._board_size:
                    return False
                if self._board[place + i][vehicle._y_coordinate] != '.':
                    return False
                i += 1
            vehicle.move_vehicle(vehicle._x_coordinate + steps_on_board, vehicle._y_coordinate)
            return True
        if move_direction == Direction.LEFT:
            i = 1
            while i <= steps_on_board:
                if vehicle._y_coordinate - i < 0:
                    return False
                if self._board[vehicle._x_coordinate][vehicle._y_coordinate - i] != '.':
                    return False
                i += 1
            vehicle.move_vehicle(vehicle._x_coordinate, vehicle._y_coordinate - steps_on_board)
            return True
        if move_direction == Direction.RIGHT:
            place = vehicle._y_coordinate + vehicle._size - 1
            i = 1
            while i <= steps_on_board:
                if place + i >= self._board_size:
                    return False
                if self._board[vehicle._x_coordinate][i + place] != '.':
                    return False
                i += 1
            vehicle.move_vehicle(vehicle._x_coordinate, vehicle._y_coordinate + steps_on_board)
            return True
        return False

    def win_state(self):
        my_vehicle = self.get_vehicle('X')
        x = my_vehicle._x_coordinate
        y = my_vehicle._y_coordinate
        if x != 2:
            return False
        else:
            while y < self._board_size:
                if self._board[x][y] != '.' and self._board[x][y] != 'X':
                    return False
                y += 1
            return True
