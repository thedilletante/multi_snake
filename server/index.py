import websockets
import asyncio
import datetime
import json

class SnakeServer:

    def __init__(self):
        self.clients = []

    async def time(self, websocket, path):
        try:
            id = hash("{}{}".format(websocket.remote_address, datetime.datetime.utcnow().isoformat()))
            await websocket.send("You id: {}".format(id))
            while True:
                now = datetime.datetime.utcnow().isoformat() + 'Z'
                message = await websocket.recv()
                print("> {}".format(message))
                await websocket.send("Fuck you {}".format(now))
        except websockets.ConnectionClosed:
            print("Client closed the connection")

if __name__ == "__main__":
    try:
        server = SnakeServer()
        start_server = websockets.serve(server.time, '', 5678)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("We've been fucked")