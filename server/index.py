import websockets
import asyncio
import datetime
from collections import namedtuple
from enum import Enum

Client = namedtuple("Client", ["id", "fd"])


class SnakeServer:

    def __init__(self):
        self.clients = []

    async def time(self, websocket, path):
        id = hash("{}{}".format(websocket.remote_address, datetime.datetime.utcnow().isoformat()))
        client = Client(id, websocket)
        self.clients.append(Client(id, websocket))

        try:
            await websocket.send("You id: {}".format(id))
            while True:
                now = datetime.datetime.utcnow().isoformat() + 'Z'
                message = await websocket.recv()
                print("> {}".format(message))
                await websocket.send("Fuck you {}".format(now))
        except websockets.ConnectionClosed:
            self.clients.remove(client)
            print("Client closed the connection")

    async def presentation_loop(self):
        while True:
            for client in self.clients:
                try:
                    await client.fd.send("New status is: I don't know")
                except websockets.ConnectionClosed:
                    print("Client closed the connection")
                    self.clients.remove(client)
            await asyncio.sleep(0.5)


if __name__ == "__main__":
    try:
        server = SnakeServer()
        start_server = websockets.serve(server.time, '', 5678)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_until_complete(asyncio.Task(server.presentation_loop()))
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("We've been fucked")


class Snake:
    def __init__(self, head_position, length, direction):
        self.body = [head_position]
        x_factor = direction.get_x_factor()
        y_factor = direction.get_y_factor()

        for i in range(0, length):
            self.body.append(Position(self.body[-1].x + x_factor, self.body[-1].y + y_factor))

    def move(self, direction):
        self.body = [self.get_new_head_position(direction)] + self.body.pop()

    def get_new_head_position(self, direction):
        return Position(self.body[0].x + direction.get_x_factor(), self.body[0].y + direction.get_y_factor())


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

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def left(self):
        return Position(self.x - 1, self.y)

    def right(self):
        return Position(self.x + 1, self.y)

    def top(self):
        return Position(self.x, self.y - 1)

    def bottom(self):
        return Position(self.x, self.y + 1)


class IntersectionCalculator:
    def __init__(self):
        pass