'''
    equipment_type.py - This file contains the EquipmentType class.
'''
from enum import auto, Enum


class EquipmentType(Enum):
    '''
        EquipmentType - This class represents the type of equipment.
    '''
    WEAPON = auto()
    ARMOR = auto()
