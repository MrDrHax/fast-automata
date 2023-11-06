from . import fastautomata_clib
from pydantic import BaseModel

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
    
class PosModel(BaseModel):
    x: int
    y: int