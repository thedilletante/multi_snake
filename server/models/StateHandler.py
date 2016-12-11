from protocol import *


class StateHandler:

    SPEED_INCREASE_FACTOR = 10

    def __init__(self, width, height, clients_info, speed=1):
        self.width = width
        self.height = height
        self.clients_info = clients_info
        self.speed = speed
        self.loose_snakes = {}
        self.step = 0
        self.partial_message = PartialStatusMessageBuilder()

    def __iter__(self):
        self.step = 0
        return self

    def __next__(self):
        snake_body_map = {}
        snake_head_map = {}
        self.loose_snakes = {}
        for id, snake in self.clients_info.items():
            snake.move()
            for position in snake.body:
                snake_body_map[position] = id
            snake_head_map[snake.body[0]] = id

        self.define_loose_snakes(snake_head_map, snake_body_map)
        for id in self.loose_snakes:
            del(self.clients_info[id])

        self.step += 1
        if self.step == StateHandler.SPEED_INCREASE_FACTOR:
            self.increase_speed()
            self.step = 0

        # generate partial result
        self.partial_message = PartialStatusMessageBuilder()
        for id, client_info in self.clients_info.items():
            self.partial_message.add_live_info(id, next(iter(client_info.body)), client_info.direction)
        for id, position in self.loose_snakes.items():
            self.partial_message.add_loose_info(id, position)

        if self.get_client_count() < 2:
            raise StopIteration()

        return self


    def turn_client(self, id, direction):
        if id in self.clients_info:
            self.clients_info[id].update(direction)

    def increase_speed(self):
        self.speed *= 2

    def get_client_count(self):
        return len(self.clients_info)

    def winner_congratulate(self):
        return winner(next(iter(self.clients_info.keys())))

    def encode_state(self):
        return self.partial_message.build()

    def initial_message(self):
        message = InitialMessageBuilder()
        for id, snake in self.clients_info.items():
            message.add_client(id, snake.head_position, snake.length, snake.direction)
        return message.build()

    def results(self):
        survived = self.get_client_count()
        return draw() if 0 == survived else self.winner_congratulate()

    def define_loose_snakes(self, head_map, body_map):
        for position, id in head_map.items():
            if position in body_map and id != body_map[position]:
                self.loose_snakes[id] = position
            if position.x < 0 or position.x > self.width or position.y < 0 or position.y > self.height:
                self.loose_snakes[id] = position
