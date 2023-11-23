import random
from bots.base_bot import BaseBot
import pygame


class ManualBot(BaseBot):
    def __init__(self, uid):
        self.rand = random.Random(uid)
        super().__init__(uid, f"{self.__class__.__name__}_{uid}", [self.rand.randrange(255) for _ in range(3)])
        self.cols = 0
        self.rows = 0
        self.cell_size = 1

    def init_board(self, cols: int, rows: int, win_length: int, obstacles: [(int, int)], time_given: int) -> None:
        self.cols = cols
        self.rows = rows
        self.cell_size = pygame.display.get_surface().get_size()[0] / cols

    def make_a_move(self, time_left: int) -> (int, int):
        x, y = -1, -1
        m_released = False
        while True:
            pygame.event.get()
            m_left, _, _ = pygame.mouse.get_pressed()
            if not m_released and m_left:
                m_left = False
            elif not m_left:
                m_released = True
            else:
                m_released = False

            if m_left:
                m_x, m_y = pygame.mouse.get_pos()
                x = int(m_x / self.cell_size)
                y = int(m_y / self.cell_size)
                break
            pygame.time.wait(50)
        return x, y
