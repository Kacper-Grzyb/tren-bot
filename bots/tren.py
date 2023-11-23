from bots.base_bot import BaseBot
import random
from game.colors import Colors
from game.board_cell import BoardCell
from datetime import datetime

class TrenBot(BaseBot):
    def __init__(self, uid) -> None:
        name = "TrenBot"
        color = (0, 255, 0) 
        super().__init__(uid, name, color)  
        self.rand = random.Random(datetime.now().timestamp())
        self.cols = 0
        self.rows = 0
        self.board = [[int]]
        self.uid = uid
        # E.g initialize extra object variables

    def init_board(self, cols: int, rows: int, win_length: int, obstacles: [(int, int)], time_given: int) -> None:
        """
        This method is invoked at the game initialization.

        Parameters:
        cols: The size of the same board in columns.
        rows: The size of the game board in rows.
        win_length: The length of the winning line.
        obstacles: The list of (x, y) coordinates of blocked board cells.
        time_given: The total time given to the player bot for the game in ns.
        """
        self.cols = cols
        self.rows = rows
        self.board = [[BoardCell.CLEAR for _ in range(rows)] for _ in range(cols)]
        for x, y in obstacles:
            self.board[x][y] = BoardCell.BLOCKED

    def make_a_move(self, time_left: int) -> (int, int):
        """
        This method is called when the bot needs to make a move. It will calculate the best move with the given board.

        Parameters:
        time_left: a value indicating time remaining for the bot to complete a game in ns

        Returns:
        tuple: containing the bot move with the order (x, y)
        """
        x = -1
        y = -1
        #I just made it return 0, 0 so our bot doesn't get immedietaly discualified
        return 0, 0

    def notify_move(self, bot_uid: int, move: (int, int)) -> None:
        """
        This method is called when a move is made by a player.

        Parameters:
        bot_uid: The Unique ID of the player making the move.
        move: A tuple representing the move coordinates (x, y).
        """
        (x, y) = move
        if self.uid != bot_uid:
            self.board[move[0]][move[1]] = BoardCell.BOT
            print(f"Bot with id {bot_uid} made a move at coordinates: {move[0]}, {move[1]}")
