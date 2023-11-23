import json
import os
from bots.base_bot import BaseBot
from bots.manual_bot import ManualBot
from bots.pedestrian_bot import PedestrianBot
from bots.random_bot import RandomBot
from bots.smart_random_bot import SmartRandomBot
from bots.tren import TrenBot  # Change this line according to the new names


class Settings:
    def __init__(self, json_file_path='settings.json'):
        # Graphics settings
        self.CELL_SIZE = 50
        self.LINE_WIDTH = 3

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_COLOR = (200, 0, 0)
        self.LINE_COLOR = (0, 0, 0)
        self.BACKGROUND_COLOR = self.WHITE
        self.WINNING_LINE_COLOR = (0, 210, 0)

        # Game settings
        self.FAST_MODE = True
        self.SHUFFLE_PLAYERS_ON_START = False
        self.CHANCE_OF_BLOCKED_ON_START = 0.05
        self.RESTART_DELAY = 0
        self.KEY_DELAY = 50
        self.GAME_TIME = 5*10**9  # play time in ns

        # Board settings
        self.BOARD_WIDTH = 15
        self.BOARD_HEIGHT = 15
        self.WIN_LENGTH = 5

        # Winning conditions
        self.WIN_HORIZONTAL = True
        self.WIN_VERTICAL = True
        self.WIN_DIAG_POS = True
        self.WIN_DIAG_NEG = True

        # Players
        self.BOTS = [
            'TrenBot',
            'RandomBot',
            'RandomBot'
        ]

        if os.path.exists(json_file_path):
            data_from_file = {}
            with open(json_file_path, 'r') as file:
                try:
                    data_from_file = json.load(file)
                except json.JSONDecodeError:
                    print("Invalid settings file")
                finally:
                    self.__dict__.update(data_from_file)

            missing_keys = set(self.__dict__) - set(data_from_file)
            if missing_keys:
                print(
                    f"Writing missing settings entries to: {json_file_path}.")
                with open(json_file_path, 'w') as file:
                    json.dump(self.__dict__, file, indent=2)
        else:
            print(f"Can't find {json_file_path}, creating a default one.")
            with open(json_file_path, 'w') as file:
                json.dump(self.__dict__, file, indent=2)

    def get_bots_as_class(self) -> list[BaseBot]:
        lst = []
        for bot in self.BOTS:
            lst.append(globals()[bot])
        return lst
