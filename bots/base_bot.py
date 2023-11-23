class BaseBot:
    def __init__(self, uid: int, name: str = "", color: (int, int, int) = (255, 0, 0)) -> None:
        self.unique_id = uid
        self.name = name
        self.color = color

    def init_board(self, cols: int, rows: int, win_length: int, obstacles: [(int, int)], time_given: int) -> None:
        pass

    def make_a_move(self, time_left: int) -> (int, int):
        return -1, -1

    def notify_move(self, bot_uid: int, move: (int, int)) -> None:
        pass
