import sys
import random
import time
from game.settings import Settings
from game.game_state import GameState
from game.board_cell import BoardCell
from game.draw import Draw
from bots.base_bot import BaseBot
from typing import Tuple
import pygame


class Game:
    def __init__(self, settings: Settings) -> None:
        self.sett = settings
        self.players = list()
        self.player_time = list()
        for i, bot in enumerate(self.sett.get_bots_as_class()):
            if issubclass(bot, BaseBot):
                self.players.append(bot(i))
                self.player_time.append(self.sett.GAME_TIME)
            else:
                print(f"{bot} is not subclass of BaseBot!")

        if self.sett.SHUFFLE_PLAYERS_ON_START:
            random.shuffle(self.players)

        # Create Board
        self.board = [[BoardCell.CLEAR for _ in range(self.sett.BOARD_HEIGHT)] for _ in range(self.sett.BOARD_WIDTH)]

        # Initialize the game variables
        self.curr_p_index = BoardCell.BOT
        self.game_ended = False
        self.winner_line = []
        self.eliminated_players = []
        self.state = GameState.INITIAL
        self.restart_time = 0
        self.drawer = Draw(self.board, self.players, self.winner_line, self.sett)

    def check_winner(self, last_move, current_player_id):
        def check_line(line):
            win_line = []
            count = 0
            for (lx, ly) in line:
                if self.board[lx][ly] == current_player_id:
                    count += 1
                    win_line.append((lx, ly))
                    if count == self.sett.WIN_LENGTH:
                        self.winner_line.extend(win_line)
                        return True
                else:
                    win_line = []
                    count = 0
            return False

        (x, y) = last_move

        row_to_check = list()
        if self.sett.WIN_HORIZONTAL:
            for i in range(-(self.sett.WIN_LENGTH - 1), self.sett.WIN_LENGTH):
                xd = x + i
                yd = y
                if xd < 0 or yd < 0 or xd >= self.sett.BOARD_WIDTH or yd >= self.sett.BOARD_HEIGHT:
                    continue
                row_to_check.append((xd, yd))
            if check_line(row_to_check):
                return True

        if self.sett.WIN_VERTICAL:
            col_to_check = list()
            for i in range(-(self.sett.WIN_LENGTH - 1), self.sett.WIN_LENGTH):
                xd = x
                yd = y + i
                if xd < 0 or yd < 0 or xd >= self.sett.BOARD_WIDTH or yd >= self.sett.BOARD_HEIGHT:
                    continue
                col_to_check.append((xd, yd))
            if check_line(col_to_check):
                return True

        if self.sett.WIN_DIAG_POS:
            diag_to_check1 = list()
            for i in range(-(self.sett.WIN_LENGTH - 1), self.sett.WIN_LENGTH):
                xd = x + i
                yd = y - i
                if xd < 0 or yd < 0 or xd >= self.sett.BOARD_WIDTH or yd >= self.sett.BOARD_HEIGHT:
                    continue
                diag_to_check1.append((xd, yd))
            if check_line(diag_to_check1):
                return True

        if self.sett.WIN_DIAG_NEG:
            diag_to_check2 = list()
            for i in range(-(self.sett.WIN_LENGTH - 1), self.sett.WIN_LENGTH):
                xd = x + i
                yd = y + i
                if xd < 0 or yd < 0 or xd >= self.sett.BOARD_WIDTH or yd >= self.sett.BOARD_HEIGHT:
                    continue
                diag_to_check2.append((xd, yd))
            if check_line(diag_to_check2):
                return True

        return False

    def register_move(self, col, row):
        if row < 0 or row >= self.sett.BOARD_HEIGHT or col < 0 or col >= self.sett.BOARD_WIDTH:
            raise ValueError(f"Cell ({col}, {row}) is outside of the playable area!")
        elif self.board[col][row] == BoardCell.BLOCKED:
            raise ValueError("Illegal move, this cell is blocked!")
        elif self.board[col][row] >= BoardCell.BOT:
            raise ValueError("Illegal move, this cell is already taken!")
        else:
            self.board[col][row] = self.curr_p_index
            if self.check_winner((col, row), self.curr_p_index):
                self.state = GameState.ENDED_WON
                return
            elif all(self.board[x][y] != BoardCell.CLEAR for y in range(self.sett.BOARD_HEIGHT) for x in range(self.sett.BOARD_WIDTH)):
                self.state = GameState.ENDED_DRAW
                return
            else:
                return

    def run(self):
        def restart_game():
            if self.sett.RESTART_DELAY < 0:
                pygame.quit()
                sys.exit()
            self.restart_time = pygame.time.get_ticks() + self.sett.RESTART_DELAY
            self.state = GameState.DELAYED_RESTART

        while True:
            match self.state:
                case GameState.INITIAL:
                    obstacles = []
                    for i in range(len(self.board)):
                        for j in range(len(self.board[i])):
                            if random.random() < self.sett.CHANCE_OF_BLOCKED_ON_START:
                                self.board[i][j] = BoardCell.BLOCKED
                                obstacles.append((i, j))
                            else:
                                self.board[i][j] = BoardCell.CLEAR
                    for i, player in enumerate(self.players):
                        try:
                            player.init_board(self.sett.BOARD_WIDTH, self.sett.BOARD_HEIGHT, self.sett.WIN_LENGTH,
                                              obstacles, self.sett.GAME_TIME)
                        except Exception as e:
                            self.eliminated_players.append(i)
                            print(f"Exception occurred during init_board(): ")
                            print(e)
                            print(f"\"{self.players[i].name}\":{self.curr_p_index} is disqualified")

                    self.drawer.draw_board(self.curr_p_index, self.state)
                    self.state = GameState.RUNNING
                case GameState.RUNNING:
                    if self.sett.FAST_MODE:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if (event.type == pygame.MOUSEBUTTONDOWN or
                            event.type == pygame.KEYDOWN or
                                self.sett.FAST_MODE):
                            try:
                                time_start = time.perf_counter_ns()
                                (x, y) = self.players[self.curr_p_index].make_a_move(0)
                                time_end = time.perf_counter_ns()
                                self.player_time[self.curr_p_index] -= time_end - time_start
                                if self.player_time[self.curr_p_index] <= 0:
                                    raise ValueError("All time budget already used!")
                                print(f"\"{self.players[self.curr_p_index].name}\" made the move: ({x},{y})")
                                self.register_move(x, y)
                            except Exception as e:
                                print(f"Exception occurred during make_a_move():")
                                print(e)
                                print(f"\"{self.players[self.curr_p_index].name}\":{self.curr_p_index} "
                                      f"is disqualified")
                                self.eliminated_players.append(self.curr_p_index)
                            else:
                                for i, player in enumerate(self.players):
                                    if i not in self.eliminated_players:
                                        try:
                                            player.notify_move(self.curr_p_index, (x, y))
                                        except Exception as e:
                                            self.eliminated_players.append(i)
                                            print(f"Exception occurred during notify_move(): ")
                                            print(e)
                                            print(f"\"{self.players[i].name}\":{self.curr_p_index} is disqualified")

                            if self.state != GameState.RUNNING:
                                break

                            for _ in self.players:
                                self.curr_p_index += 1
                                if self.curr_p_index >= len(self.players):
                                    self.curr_p_index = 0
                                if self.curr_p_index not in self.eliminated_players:
                                    break
                            else:
                                self.state = GameState.ENDED_LOST

                        self.drawer.draw_board(self.curr_p_index, self.state)

                case GameState.ENDED_WON:
                    print(f"\"{self.players[self.curr_p_index].name}\" wins the game")
                    self.drawer.draw_board(self.curr_p_index, self.state)
                    restart_game()
                case GameState.ENDED_DRAW:
                    print("It's a draw!")
                    self.drawer.draw_board(self.curr_p_index, self.state)
                    restart_game()
                case GameState.ENDED_LOST:
                    print("Can't find another player")
                    print(f"Eliminated players: {self.eliminated_players}")
                    self.drawer.draw_board(self.curr_p_index, self.state)
                    restart_game()
                case GameState.DELAYED_RESTART:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    keys = pygame.key.get_pressed()
                    if self.sett.RESTART_DELAY > 0:
                        if keys[pygame.K_SPACE]:
                            self.restart_time += self.sett.KEY_DELAY

                        if self.restart_time < pygame.time.get_ticks():
                            break
                    else:
                        if keys[pygame.K_SPACE]:
                            pygame.time.wait(5*self.sett.KEY_DELAY)
                            break
                    pygame.time.wait(self.sett.KEY_DELAY)
                case _:
                    print("Invalid game state!")
                    break
