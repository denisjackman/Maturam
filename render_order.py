'''
    render order
'''
from enum import auto, Enum


class RenderOrder(Enum):
    '''
        render order class
    '''
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
