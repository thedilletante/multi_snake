from enum import Enum


class Direction(Enum):
    top = 0
    left = 1
    bottom = 2
    right = 3

    def get_x_factor(self):
        if self == Direction.left:
            return -1
        if self == Direction.right:
            return 1
        return 0

    def get_y_factor(self):
        if self == Direction.top:
            return -1
        if self == Direction.bottom:
            return 1
        return 0

    def __str__(self):
        if self == Direction.top:
            return "TOP"
        elif self == Direction.left:
            return "LEFT"
        elif self == Direction.bottom:
            return "BOTTOM"
        elif self == Direction.right:
            return "RIGHT"
        return "UNKNOWN_DIRECTION"

    @staticmethod
    def create(str_direction):
        if str_direction == "TOP":
            return Direction.top
        elif str_direction == "LEFT":
            return Direction.left
        elif str_direction == "BOTTOM":
            return Direction.bottom
        elif str_direction == "RIGHT":
            return Direction.right
        raise Exception()
