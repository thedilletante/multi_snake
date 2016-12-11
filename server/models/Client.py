from json import loads
from models import Direction


class Client:
    def __init__(self, id, fd):
        self.id = id
        self.fd = fd
        self.boards = []

    def add_game_board(self, board):
        self.boards.append(board)

    def received_command(self, command):
        decoded = loads(command)
        direction = Direction.create(decoded["direction"])
        for board in self.boards:
            board.turn_client(self.id, direction)