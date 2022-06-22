'''
    This is the general entity class
'''
from typing import Tuple


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self,
                 x: int,  # pylint: disable C0103
                 y: int,  # pylint: disable C0103
                 char: str,
                 color: Tuple[int, int, int]):
        self.x = x  # pylint: disable C0103
        self.y = y  # pylint: disable C0103
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:   # pylint: disable C0103
        '''
            Move the entity by a given amount
        '''
        self.x += dx
        self.y += dy
