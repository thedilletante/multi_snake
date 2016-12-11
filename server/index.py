import websockets
import asyncio
import logging
from models import Server


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

    host = ""
    port = 5678
    try:
        server = Server(asyncio.get_event_loop())
        start_server = websockets.serve(server.on_client_connect, host, port)

        asyncio.get_event_loop().run_until_complete(start_server)
        logging.debug("Started game server: {}:{}".format(host, port))
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logging.debug("The game server was shut")
