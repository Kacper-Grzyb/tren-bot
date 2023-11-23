import random
from bots.base_bot import BaseBot
from game.board_cell import BoardCell
from game.colors import Colors
from datetime import datetime


class SmartRandomBot(BaseBot):
    def __init__(self, uid):
        self.rand = random.Random(datetime.now().timestamp())
        super().__init__(uid, f"{self.__class__.__name__}_{uid}", Colors.get_random_color())
        self.cols = 0
        self.rows = 0
        self.board = [[int]]

    def init_board(self, cols: int, rows: int, win_length: int, obstacles: [(int, int)], time_given: int) -> None:
        self.cols = cols
        self.rows = rows
        self.board = [[BoardCell.CLEAR for _ in range(rows)] for _ in range(cols)]
        for x, y in obstacles:
            self.board[x][y] = BoardCell.BLOCKED

    def make_a_move(self, time_left: int) -> (int, int):
        width = self.cols
        height = self.rows
        for _ in range(width * height):
            x = self.rand.randrange(width)
            y = self.rand.randrange(height)
            if self.board[x][y] == BoardCell.CLEAR:
                return x, y
        return -1, -1

    def notify_move(self, bot_uid: int, move: (int, int)) -> None:
        (x, y) = move
        self.board[x][y] = bot_uid
