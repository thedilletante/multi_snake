import asyncio
import logging
import websockets

from models.Direction import Direction
from models.Snake import Snake
from models.StateHandler import StateHandler
from models.Snake import Position


class Game:

    DEFAULT_HEIGHT = 100
    DEFAULT_WIDTH = 100
    REFRESH_TIMEOUT = 0.2
    NUM_CLIENTS_TO_GAME = 2

    def __init__(self, clients, loop):
        self.clients = clients
        self.loop = loop
        self.game_id = "".join((str(client.id) for client in self.clients))

    @asyncio.coroutine
    def start(self):
        logging.debug("Game session started")
        try:
            board = self.build_the_board()
            yield from self.broadcast(board.initial_message())
            for board_state in board:
                yield from self.broadcast(board_state.encode_state())
                yield from asyncio.sleep(Game.REFRESH_TIMEOUT)
            yield from self.broadcast(board.results())

        except websockets.ConnectionClosed:
            logging.debug("Client disconnected, game is over".format())
        finally:
            self.end_game()

    @asyncio.coroutine
    def broadcast(self, message):
        logging.debug("Game({}): Broadcast message: {}".format(self.game_id, message))
        for client in self.clients:
            yield from client.fd.send(message)

    def end_game(self):
        for client in self.clients:
            asyncio.ensure_future(client.fd.close(), loop=self.loop)

    def build_the_board(self):
        clients_info = {}

        for index, client in enumerate(self.clients):
            head = Position(40 + 20 * index, 40 + 20 * index)
            direction = Direction.left if index == 0 else Direction.right
            clients_info[client.id] = Snake(client.id, head, direction=direction)

        board = StateHandler(Game.DEFAULT_HEIGHT,
                             Game.DEFAULT_WIDTH,
                             clients_info)

        for client in self.clients:
            client.add_game_board(board)

        return board
