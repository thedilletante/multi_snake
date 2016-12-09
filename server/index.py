import websockets
import asyncio
import random
import datetime


@asyncio.coroutine
def hello(websocket, path):
    name = yield from websocket.recv()
    print("< {}".format(name))

    greeting = "Hello {}!".format(name)
    yield from websocket.send(greeting)
    print("> {}".format(greeting))

@asyncio.coroutine
def time(websocket, path):
    try:
        while True:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            message = yield from websocket.recv()
            print("> {}".format(message))
            yield from websocket.send("Fuck you {}".format(now))
            # yield from asyncio.sleep(random.random() * 3)
    except websockets.ConnectionClosed:
        print("Client closed the connection")

if __name__ == "__main__":
    # start_server = websockets.serve(hello, 'localhost', 8765)
    #
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()

    start_server = websockets.serve(time, '127.0.0.1', 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()