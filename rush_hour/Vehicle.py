from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Vehicle:

    def __init__(self, size, name, orientation, x, y):
        self._size = size
        self._name = name
        self._orientation = orientation
        self._x_coordinate = x
        self._y_coordinate = y

    def move_vehicle(self, x, y):
        self._x_coordinate = x
        self._y_coordinate = y

    def get_name(self):
        return self._name

    def get_orientation(self):
        return self._orientation

    def get_x_coordinate(self):
        return self._x_coordinate

    def get_y_coordinate(self):
        return self._y_coordinate

    def get_size(self):
        return self._size
