from enum import Enum, auto

class SpaceType(Enum):
    SALARY = auto()
    RAND_EVENT = auto()

class Space:
    def __init__(self, type):
        self.type = type

class Board:
    def __init__(self):
        self.spaces = []
        for _ in range(4):
            self.spaces.extend([Space(SpaceType.SALARY)] + [Space(SpaceType.RAND_EVENT) for _ in range(6)])


    