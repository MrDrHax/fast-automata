from collections.abc import Callable
from typing import Any
from . import fastautomata_clib
from pydantic import BaseModel
import json, enum

class PosJSONEnconderTypes(enum.Enum):
    ARRAY = 0
    TUPLE = 1
    DICT = 2

pos_json_encoder_config = PosJSONEnconderTypes.TUPLE

class Pos(fastautomata_clib.Pos):
    '''
    A pythonic wrapper for the clib Pos
    '''
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __str__(self) -> str:
        return f'Pos({self.x}, {self.y})'
    
    def __repr__(self) -> str:
        return f'<Pos({self.x}, {self.y})>'
    
    def to_array(self) -> list[int]:
        return [self.x, self.y]
    
    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def to_dict(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y}
    
    @classmethod
    def from_array(cls, array: list[int]) -> 'Pos':
        return cls(array[0], array[1])

    @classmethod
    def from_tuple(cls, tuple: tuple[int, int]) -> 'Pos':
        return cls(tuple[0], tuple[1])

    @classmethod
    def from_dict(cls, dict: dict[str, int]) -> 'Pos':
        return cls(dict["x"], dict["y"]) 

class PosJSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Pos):
            global pos_json_encoder_config
            if pos_json_encoder_config == PosJSONEnconderTypes.ARRAY:
                return obj.to_array()
            elif pos_json_encoder_config == PosJSONEnconderTypes.DICT:
                return obj.to_dict()
            elif pos_json_encoder_config == PosJSONEnconderTypes.TUPLE:
                return obj.to_tuple()
            else:
                raise TypeError("Invalid PosJSONEnconderTypes")
            
        if isinstance(obj, fastautomata_clib.Pos):
            return (obj.x, obj.y)
            
        return super().default(obj)
    
    @classmethod
    def decode(cls, obj):
        if isinstance(obj, list):
            if len(obj) == 2 and isinstance(obj[0], int) and isinstance(obj[1], int):
                return Pos.from_array(obj)
            return [Pos.from_array(x) for x in obj]

        return obj

class PosModel(BaseModel):
    x: int
    y: int