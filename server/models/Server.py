import websockets
import asyncio
import datetime
import logging
from json import loads
from protocol import *
from models import *


class Server:

    REFRESH_TIMEOUT = 0.05
    NUM_CLIENTS_TO_GAME = 2

    def __init__(self, loop):
        self.clients = []
        self.loop = loop
        self.game_started = False

    @asyncio.coroutine
    def on_client_connect(self, websocket, path):
        logging.debug("New connection from: {}".format(websocket.remote_address))

        if self.game_started:
            websocket.send(busy())
            return

        id = hash("{}{}".format(websocket.remote_address, datetime.datetime.utcnow().isoformat()))
        client = Client(id, websocket)
        self.clients.append(client)
        logging.debug("Client({}) added for game, active: {}".format(id, len(self.clients)))

        try:
            yield from websocket.send(greeting(id))

            while not self.game_started:
                yield from asyncio.sleep(Server.REFRESH_TIMEOUT)

            while True:
                message = yield from websocket.recv()
                logging.debug("Client({}) sent an request: {}".format(id, message))
                decoded = loads(message)
                direction = Direction.create(decoded["direction"])
                self.board.turn_client(id, direction)
        except websockets.ConnectionClosed:
            logging.debug("Client({}) disconnected".format(id))

    @asyncio.coroutine
    def presentation_loop(self):
        while True:
            try:
                while len(self.clients) != Server.NUM_CLIENTS_TO_GAME:
                    yield from asyncio.sleep(Server.REFRESH_TIMEOUT)

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
                    yield from client.fd.send(initial_message)

                self.board = StateHandler(100, 100, clients_info)

                # the game loop
                self.game_started = True
                for board_state in self.board:

                    state = board_state.encode_state()
                    for client in self.clients:
                        yield from client.fd.send(state)

                    yield from asyncio.sleep(Server.REFRESH_TIMEOUT)

                # tell the result
                survived = self.board.get_client_count()
                if survived == 1:
                    for client in self.clients:
                        yield from client.fd.send(self.board.winner_congratulate())
                elif survived == 0:
                    for client in self.clients:
                        yield from client.fd.send(draw())

                logging.debug("Game is over")
            except websockets.ConnectionClosed:
                logging.debug("Client disconnected, game is over".format())
            finally:
                self.clients = []
                self.game_started = False