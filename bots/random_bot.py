import random
from bots.base_bot import BaseBot
from game.colors import Colors


class RandomBot(BaseBot):
    def __init__(self, uid):
        self.rand = random.Random(uid)
        super().__init__(uid, f"{self.__class__.__name__}_{uid}", Colors.get_random_color())
        self.cols = 0
        self.rows = 0

    def init_board(self, cols: int, rows: int, win_length: int, obstacles: [(int, int)], time_given: int) -> None:
        self.cols = cols
        self.rows = rows

    def make_a_move(self, time_left: int) -> (int, int):
        x = self.rand.randrange(self.cols)
        y = self.rand.randrange(self.rows)
        return x, y
