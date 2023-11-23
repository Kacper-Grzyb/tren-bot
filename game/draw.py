import pygame
from game.game_state import GameState
from game.board_cell import BoardCell
from game.settings import Settings


class Draw:
    def __init__(self, board, players, winner_line, settings: Settings) -> None:
        self.sett = settings
        self.board = board
        self.players = players
        self.winner_line = winner_line
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.sett.CELL_SIZE * self.sett.BOARD_WIDTH, self.sett.CELL_SIZE * self.sett.BOARD_HEIGHT))
        pygame.display.set_caption(f"{self.sett.WIN_LENGTH} in A Line")
        self.font = pygame.font.Font(None, int(self.sett.CELL_SIZE / 2))

    def draw_board(self, curr_p_index, state):
        self.screen.fill(self.sett.WHITE)
        for i in range(1, self.sett.BOARD_WIDTH):
            pygame.draw.line(self.screen, self.sett.LINE_COLOR, (self.sett.CELL_SIZE * i, 0),
                             (self.sett.CELL_SIZE * i, self.sett.CELL_SIZE * self.sett.BOARD_HEIGHT), self.sett.LINE_WIDTH)
        for i in range(1, self.sett.BOARD_HEIGHT):
            pygame.draw.line(self.screen, self.sett.LINE_COLOR, (0, self.sett.CELL_SIZE * i),
                             (self.sett.CELL_SIZE * self.sett.BOARD_WIDTH, self.sett.CELL_SIZE * i), self.sett.LINE_WIDTH)

        for row in range(self.sett.BOARD_HEIGHT):
            for col in range(self.sett.BOARD_WIDTH):
                cell_content = self.board[col][row]
                if cell_content == BoardCell.BLOCKED:
                    self.draw_blocked(row, col)
                elif cell_content >= BoardCell.BOT:
                    self.draw_move(row, col, int(cell_content),
                                   color=self.players[cell_content].color)

        if state == GameState.ENDED_WON:
            self.draw_winning_line()
            self.draw_winner_text(
                f"\"{self.players[curr_p_index].name}\" wins the game!")
        elif state == GameState.ENDED_DRAW:
            self.draw_winner_text("Draw!")
        elif state == GameState.ENDED_LOST:
            self.draw_winner_text("All lost!!")

        pygame.display.flip()

    def draw_blocked(self, row, col):
        x_pos = col * self.sett.CELL_SIZE
        y_pos = row * self.sett.CELL_SIZE

        pygame.draw.rect(self.screen, self.sett.BLACK, (x_pos,
                         y_pos, self.sett.CELL_SIZE, self.sett.CELL_SIZE))

    def draw_move(self, row, col, player, color=(255, 255, 255)):
        x_pos = col * self.sett.CELL_SIZE + self.sett.CELL_SIZE // 2
        y_pos = row * self.sett.CELL_SIZE + self.sett.CELL_SIZE // 2
        half_size = self.sett.CELL_SIZE // 2 - 10
        pygame.draw.line(self.screen, color, (x_pos - half_size, y_pos - half_size),
                         (x_pos + half_size, y_pos + half_size), self.sett.LINE_WIDTH * 2)
        pygame.draw.line(self.screen, color, (x_pos + half_size, y_pos - half_size),
                         (x_pos - half_size, y_pos + half_size), self.sett.LINE_WIDTH * 2)

        text = self.font.render(str(player), True, self.sett.BLACK)
        text_rect = text.get_rect(
            center=(x_pos + self.sett.CELL_SIZE // 5, y_pos))

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)

    def draw_winning_line(self):
        start_cell = self.winner_line[0]
        end_cell = self.winner_line[-1]
        start_pos = (start_cell[0] * self.sett.CELL_SIZE + self.sett.CELL_SIZE //
                     2, start_cell[1] * self.sett.CELL_SIZE + self.sett.CELL_SIZE // 2)
        end_pos = (end_cell[0] * self.sett.CELL_SIZE + self.sett.CELL_SIZE // 2,
                   end_cell[1] * self.sett.CELL_SIZE + self.sett.CELL_SIZE // 2)

        border_color = self.sett.BLACK
        border_width = 1
        line_width = self.sett.LINE_WIDTH

        pygame.draw.line(self.screen, border_color, (start_pos[0] - border_width, start_pos[1]), (
            end_pos[0] - border_width, end_pos[1]), line_width + 2 * border_width)
        pygame.draw.line(self.screen, border_color, (start_pos[0] + border_width, start_pos[1]), (
            end_pos[0] + border_width, end_pos[1]), line_width + 2 * border_width)
        pygame.draw.line(self.screen, border_color, (start_pos[0], start_pos[1] - border_width), (
            end_pos[0], end_pos[1] - border_width), line_width + 2 * border_width)
        pygame.draw.line(self.screen, border_color, (start_pos[0], start_pos[1] + border_width), (
            end_pos[0], end_pos[1] + border_width), line_width + 2 * border_width)

        pygame.draw.line(self.screen, self.sett.WINNING_LINE_COLOR,
                         start_pos, end_pos, line_width)

    def draw_winner_text(self, msg):
        text = self.font.render(msg, True, self.sett.FONT_COLOR)
        text_rect = text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        offset = self.sett.CELL_SIZE // 15
        pygame.draw.rect(self.screen, self.sett.BACKGROUND_COLOR, (text_rect.left - offset,
                                                                   text_rect.top - offset,
                                                                   text_rect.width + offset * 2,
                                                                   text_rect.height + offset * 2))

        # Draw the text
        self.screen.blit(text, text_rect)
