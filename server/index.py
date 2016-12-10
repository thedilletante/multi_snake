import websockets
import asyncio
import datetime
import logging

from json import loads
from collections import namedtuple
from enum import Enum
from protocol import *

Client = namedtuple("Client", ["id", "fd"])
Position = namedtuple("Position", ["x", "y"])

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

class Snake:
    def __init__(self, head_position, length, direction):
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


class GameBoard:

    SPEED_INCREASE_FACTOR = 50


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
        if self.step == GameBoard.SPEED_INCREASE_FACTOR:
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

    def define_loose_snakes(self, head_map, body_map):
        for position, id in head_map.items():
            if position in body_map and id != body_map[position]:
                self.loose_snakes[id] = position
            if position.x < 0 or position.x > self.width or position.y < 0 or position.y > self.height:
                self.loose_snakes[id] = position


class SnakeServer:

    REFRESH_TIMEOUT = 0.2
    NUM_CLIENTS_TO_GAME = 2

    def __init__(self, loop):
        self.clients = []
        self.loop = loop
        self.game_started = False

    async def on_client_connect(self, websocket, path):
        logging.debug("New connection from: {}".format(websocket.remote_address))

        if self.game_started:
            websocket.send(busy())
            return

        id = hash("{}{}".format(websocket.remote_address, datetime.datetime.utcnow().isoformat()))
        client = Client(id, websocket)
        self.clients.append(client)
        logging.debug("Client({}) added for game, active: {}".format(id, len(self.clients)))

        try:
            await websocket.send(greeting(id))

            while not self.game_started:
                await asyncio.sleep(SnakeServer.REFRESH_TIMEOUT)

            while True:
                message = await websocket.recv()
                logging.debug("Client({}) sent an request: {}".format(id, message))
                decoded = loads(message)
                direction = Direction.create(decoded["direction"])
                self.board.turn_client(id, direction)
        except websockets.ConnectionClosed:
            logging.debug("Client({}) disconnected".format(id))

    async def presentation_loop(self):
        while True:
            try:
                while len(self.clients) != SnakeServer.NUM_CLIENTS_TO_GAME:
                    await asyncio.sleep(SnakeServer.REFRESH_TIMEOUT)

                logging.debug("Game session started")

                clients_info = {}
                initial_state = InitialMessageBuilder()
                for index, client in enumerate(self.clients):
                    head = Position(40 + 20 * index, 40 + 20 * index)
                    length = 20
                    direction = Direction.left if index == 0 else Direction.right
                    clients_info[client.id] = Snake(head, length, direction)
                    initial_state.add_client(client.id, head, length, direction)

                initial_message = initial_state.build()

                for client in self.clients:
                    await client.fd.send(initial_message)

                self.board = GameBoard(100, 100, clients_info)

                # the game loop
                self.game_started = True
                for board_state in self.board:

                    state = board_state.encode_state()
                    for client in self.clients:
                        await client.fd.send(state)

                    await asyncio.sleep(SnakeServer.REFRESH_TIMEOUT)

                # tell the result
                survived = self.board.get_client_count()
                if survived == 1:
                    for client in self.clients:
                        await client.fd.send(self.board.winner_congratulate())
                elif survived == 0:
                    for client in self.clients:
                        await client.fd.send(draw())

                logging.debug("Game is over")
            except websockets.ConnectionClosed:
                logging.debug("Client disconnected, game is over".format())
            finally:
                self.clients = []
                self.game_started = False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

    host = ""
    port = 5678
    try:
        server = SnakeServer(asyncio.get_event_loop())
        start_server = websockets.serve(server.on_client_connect, host, port)

        asyncio.get_event_loop().run_until_complete(start_server)
        logging.debug("Started game server: {}:{}".format(host, port))
        # TODO:  refactor it
        # game loop should be started after client connections
        asyncio.get_event_loop().run_until_complete(asyncio.Task(server.presentation_loop()))
        logging.debug("Presentation loop started")
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logging.debug("The game server was shut")
