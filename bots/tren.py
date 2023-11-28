from bots.base_bot import BaseBot
import random
from game.colors import Colors
from game.board_cell import BoardCell
from datetime import datetime

class TrenBot(BaseBot):
    def __init__(self, uid) -> None:
        name = "TrenBot"
        color = (255, 56, 152) 
        super().__init__(uid, name, color)  
        self.rand = random.Random(datetime.now().timestamp())
        self.cols = 0
        self.rows = 0
        self.board = [[int]]
        self.uid = uid
        self.winLength = 3
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
        self.winLength = win_length
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
    
    def interrupt_win(self, time_left: int) -> None:
        nextID = self.uid+1
        # now check for lines in each direction from the placed point to know if player is going to win
        # this is definitely not the most optimal way of doing this shit but it works
        # check vertically down
        i = 1
        while x+1>len(self.board) and i<self.winLength:
            x+=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        if i == self.winLength-1:
            # store somewhere that player bot_uid is about to win
            pass
        
        # check vertically up
        i = 1
        while x-1>0 and i<self.winLength:
            x-=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        if i == self.winLength-1:
            # store somewhere that player bot_uid is about to win
            pass
        
        # check horizontally right
        i = 1
        while y+1<len(self.board[x]) and i<self.winLength:
            y+=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        if i == self.winLength-1:
            # store somewhere that player bot_uid is about to win
            pass
        
        # check horizontally left
        i = 1
        while y-1>0 and i<self.winLength:
            y-=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        if i == self.winLength-1:
            # store somewhere that player bot_uid is about to win
            pass
        
        # check diagonally up and right
        i=1
        while x+1<len(self.board) and y-1>0 and i<self.winLength:
            x+=1
            y-=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        if i == self.winLength-1:
            # store somewhere that player bot_uid is about to win
            pass
        
        # check diagonally up and left
        i=1
        while x-11>0 and y-1>0 and i<self.winLength:
            x-=1
            y-=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        if i == self.winLength-1:
            # store somewhere that player bot_uid is about to win
            pass
        
        # check diagonally down and right
        i=1
        while x+1<len(self.board) and y+1<len(self.board[x]) and i<self.winLength:
            x+=1
            y+=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        if i == self.winLength-1:
            # store somewhere that player bot_uid is about to win
            pass
        
        # check diagonally down and left
        i=1
        while x-1>0 and y+1<len(self.board[x]) and i<self.winLength:
            x-=1
            y+=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        if i == self.winLength-1:
            # store somewhere that player bot_uid is about to win
            pass        

                
            

    def notify_move(self, bot_uid: int, move: (int, int)) -> None:
        """
        This method is called when a move is made by a player.

        Parameters:
        bot_uid: The Unique ID of the player making the move.
        move: A tuple representing the move coordinates (x, y).
        """
        (x, y) = move
        if self.uid != bot_uid:
            self.board[x][y] = bot_uid
            #print(f"Bot with id {bot_uid} made a move at coordinates: {x}, {y}")
        
        
        
        
        
            
            
           
