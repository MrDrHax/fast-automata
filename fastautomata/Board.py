from . import fastautomata_clib

class SimulatedBoard(fastautomata_clib.SimulatedBoard):
    '''
    A pythonic wrapper for the clib board
    '''
    specialValues: dict[str, any] = {}

    def __init__(self, width: int, height: int, states: int):
        super().__init__(width, height, states)
        self.specialValues = {}

    def __str__(self) -> str:
        return f'SimulatedBoard({self.getWidth()}, {self.getHeight()}, {self.getLayerCount()})'
    
    def __repr__(self) -> str:
        return f'<SimulatedBoard({self.getWidth()}, {self.getHeight()}, {self.getLayerCount()})>'
    