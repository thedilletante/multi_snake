from collections import namedtuple
from models.Direction import Direction

Position = namedtuple("Position", ["x", "y"])


class Snake:
    DEFAULT_LENGTH = 20
    DEFAULT_DIRECTION = Direction.left

    def __init__(self, id, head_position, length=DEFAULT_LENGTH, direction=DEFAULT_DIRECTION):
        self.id = id
        self.head_position = head_position
        self.body = [head_position]
        self.direction = direction
        self.length = length

        x_factor = direction.get_x_factor()
        y_factor = direction.get_y_factor()
        for i in range(0, length):
            self.body.append(Position(self.body[-1].x - x_factor, self.body[-1].y - y_factor))

    def move(self, speed=1):
        for i in range(0, speed):
            self.body.pop()  # TODO: avoid of pessimisation
            self.body = [self.get_new_head_position()] + self.body

    def get_new_head_position(self, speed=1):
        return Position(self.body[0].x + speed * self.direction.get_x_factor(),
                        self.body[0].y + speed * self.direction.get_y_factor())

    def update(self, direction):
        self.direction = direction
