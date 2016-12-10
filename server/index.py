import websockets
import asyncio
import datetime

from collections import namedtuple

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