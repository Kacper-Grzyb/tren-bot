from asyncio.windows_events import NULL
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

    def interrupt_win(self, startX, startY, checkedSpots) -> (int, int):
        (x, y) = (startX, startY)
        nextID = self.uid+1
        # now check for lines in each direction from the placed point to know if player is going to win
        # this is definitely not the most optimal way of doing this shit but it works

        # check vertically down
        i = 1
        while x+1>len(self.board):
            checkedSpots[x][y] = True
            if i==self.winLength-1:
                return x+1, y
            x+=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        
        # check vertically up
        i = 1
        x, y = startX, startY
        while x-1>0:
            checkedSpots[x][y] = True
            if i == self.winLength-1:
                return x-1, y
            x-=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        
        # check horizontally right
        i = 1
        x, y = 0, 0
        while y+1<len(self.board[x]):
            checkedSpots[x][y] = True
            if i == self.winLength-1:
                return x, y+1
            y+=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        
        # check horizontally left
        i = 1
        x, y = startX, startY
        while y-1>0:
            checkedSpots[x][y] = True
            if i == self.winLength-1:
                return x, y-1
            y-=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        
        # check diagonally up and right
        i=1
        x, y = startX, startY
        while x+1<len(self.board) and y-1>0:
            checkedSpots[x][y] = True
            if(i == self.winLength):
                return x+1, y-1
            x+=1
            y-=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        
        # check diagonally up and left
        i=1
        x, y = startX, startY
        while x-1>0 and y-1>0 and i<self.winLength:
            checkedSpots[x][y] = True
            if i == self.winLength-1:
                return x-1, y-1
            x-=1
            y-=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        
        # check diagonally down and right
        i=1
        x, y = startX, startY
        while x+1<len(self.board) and y+1<len(self.board[x]) and i<self.winLength:
            checkedSpots[x][y] = True
            if i == self.winLength-1:
                return x+1, y+1
            x+=1
            y+=1
            if(self.board[x][y]!=nextID):
                break
            i+=1
        
        # check diagonally down and left
        i=1
        x, y = startX, startY
        while x-1>0 and y+1<len(self.board[x]) and i<self.winLength:
            checkedSpots[x][y] = True
            if i == self.winLength-1:
                return x-1, y+1
            x-=1
            y+=1
            if(self.board[x][y]!=nextID):
                break
            i+=1  
            
        return NULL, NULL

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

    
    def score(self):
        score = 0
        for row in self.board:
            for cell in row:
                if cell == self.uid: 
                    score += 1
                else: 
                    score -= 1
        return score

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return self.score()

        if maximizingPlayer:
            maxEval = float('-inf')
            for x in range(len(self.board)):
                for y in range(len(self.board[x])):
                    if self.board[x][y] == BoardCell.CLEAR:
                        self.board[x][y] = self.uid  # Player's move
                        eval = self.minimax(depth - 1, alpha, beta, False)
                        self.board[x][y] = BoardCell.CLEAR  # Undo move
                        maxEval = max(maxEval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return maxEval

        else:  # Minimizing player
            minEval = float('inf')
            for x in range(len(self.board)):
                for y in range(len(self.board[x])):
                    if self.board[x][y] == BoardCell.CLEAR:
                        self.board[x][y] = -1  # Opponent's move
                        eval = self.minimax(depth - 1, alpha, beta, True)
                        self.board[x][y] = BoardCell.CLEAR  # Undo move
                        minEval = min(minEval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return minEval


    def find_best_move(self):
        bestScore = float('-inf')
        move = (0, 0)
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] == BoardCell.CLEAR:
                    self.board[x][y] = self.uid
                    score = self.minimax(1, float('-inf'), float('-inf'), False)
                    self.board[x][y] = BoardCell.CLEAR
                    if score > bestScore:
                        bestScore = score
                        move = (x, y)

        return move

    def make_a_move(self, time_left: int) -> (int, int):
        """
        This method is called when the bot needs to make a move. It will calculate the best move with the given board.

        Parameters:
        time_left: a value indicating time remaining for the bot to complete a game in ns

        Returns:
        tuple: containing the bot move with the order (x, y)
        
        checkedSpots = [[False for _ in range(self.rows)] for _ in range(self.rows)]
        (x, y) = NULL, NULL
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if(self.board[i][j]==self.uid+1 and checkedSpots[i][j]==False):
                    print(f"Blocking move at {i} {j}")
                    (x, y) = self.interrupt_win(i, j, checkedSpots)
                    checkedSpots[x][y]=True
                    
        if (x, y) != (NULL, NULL) and self.isValidMove(x, y):
            return x, y
            #print(f"Blocked a line on {x},{y}")
        else:
            while(not self.isValidMove(x, y)):
                x = random.randrange(0, len(self.board))
                y = random.randrange(0, len(self.board[x]))
        return x, y 
        """

        return self.find_best_move()

                
    def isValidMove(self, col: int, row: int) -> bool:
        return row >=0 and row < len(self.board[col]) and col >= 0 and col < len(self.board) and self.board[col][row] == BoardCell.CLEAR
    

    def notify_move(self, bot_uid: int, move: (int, int)) -> None:
        """
        This method is called when a move is made by a player.
        """
        (x, y) = move
        self.board[x][y] = bot_uid
        
        
        
        
        
            
            
           
