from enum import Enum


class GameState(Enum):
    INITIAL = 0
    RUNNING = 1
    ENDED_WON = 2
    ENDED_DRAW = 3
    ENDED_LOST = 4
    DELAYED_RESTART = 5
