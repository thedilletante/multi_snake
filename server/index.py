import websockets
import asyncio
import datetime

async def time(websocket, path):
    try:
        while True:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            message = await websocket.recv()
            print("> {}".format(message))
            await websocket.send("Fuck you {}".format(now))
    except websockets.ConnectionClosed:
        print("Client closed the connection")

if __name__ == "__main__":
    try:
        start_server = websockets.serve(time, '127.0.0.1', 5678)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("We've been fucked")