from json import dumps


def greeting(id):
    return dumps({"type":"greeting",
                  "id": id})


class InitialMessageBuilder:

    def __init__(self):
        self.clients = {}

    def add_client(self, id, head, length, direction):
        self.clients[id] = {
            "head": {"x": head.x, "y": head.y},
            "length": length,
            "direction": str(direction)
        }

    def build(self):
        return dumps({"type": "initial",
                      "info": self.clients})


class PartialStatusMessageBuilder:

    def __init__(self):
        self.loose_info = {}
        self.live_info = {}

    def add_loose_info(self, id, head):
        self.loose_info[id] = {
            "head": {"x": head.x, "y": head.y},
        }

    def add_live_info(self, id, head, direction):
        self.live_info[id] = {
            "head": {"x": head.x, "y": head.y},
            "direction": str(direction)
        }

    def build(self):
        return dumps({"type": "partial",
                      "loose_info": self.loose_info,
                      "live_info": self.live_info})


def winner(id):
    return dumps({"type": "winner",
                  "id": id})


def draw():
    return dumps({"type": "draw"})


def busy():
    return dumps({"type": "busy"})