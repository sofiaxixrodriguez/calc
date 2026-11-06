from enum import Enum

class Modes(Enum):
    BASE = "base"
    SCIENTIFIC = "cien"
    PROGRAMMING = "prog"


class Operations(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "x"
    DIVIDE = "/"

    POWER = "p"
    FACTORIAL = "f"
    SQUARE_ROOT = "r"
    SECOND_DEGREE = "s"

    DECIMAL_TO_HEX = "hex"

    EXIT = "="
    NONE = "none"


class EventType(Enum):
    MODE = 0
    OPERATION = 1
    DATA = 2
    RESULT = 3
    MESSAGE = 4


class OutputType(Enum):
    MAIN_MENU = 0
    MODE_MENU = 1
    DATA_REQUEST = 2
    RESULT = 3
    ERROR = 4


class ResultSelection(Enum):
    X1 = "x1"
    X2 = "x2"
    DISCARD = "n"