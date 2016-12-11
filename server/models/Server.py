import asyncio
import datetime
import logging
import websockets

from models.Game import Game
from models.Client import Client
from protocol import greeting


class Server:

    def __init__(self, loop):
        self.pending_clients = []
        self.loop = loop

    @asyncio.coroutine
    def on_client_connect(self, websocket, path):
        logging.debug("New connection from: {}".format(websocket.remote_address))

        id = hash("{}{}".format(websocket.remote_address, datetime.datetime.utcnow().isoformat()))
        client = Client(id, websocket)

        if len(self.pending_clients) == (Game.NUM_CLIENTS_TO_GAME - 1):
            # start the game
            logging.debug("Start the new game")
            players = [client] + self.pending_clients
            self.pending_clients = []
            asyncio.ensure_future(Game(players, self.loop).start(), loop=self.loop)
            logging.debug("New game session was started")
        else:
            self.pending_clients.append(client)

        try:
            yield from websocket.send(greeting(id))

            while True:
                message = yield from websocket.recv()
                logging.debug("Client({}) sent an request: {}".format(id, message))
                client.received_command(message)
        except websockets.ConnectionClosed:
            logging.debug("Client({}) disconnected".format(id))
            if client in self.pending_clients:
                self.pending_clients.remove(client)