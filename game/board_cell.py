from enum import IntEnum


class BoardCell(IntEnum):
    BLOCKED = -2
    CLEAR = -1
    BOT = 0
