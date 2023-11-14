from . import fastautomata_clib
import typing
class SimulatedBoard(fastautomata_clib.SimulatedBoard):
    '''
    A pythonic wrapper for the clib board

    Contains stepping and resetting methods.
    '''
    specialValues: dict[str, any] = {}

    simulated: bool = True

    python_delete_agents: typing.Callable[[], None] = None

    def __init__(self, width: int, height: int, layers: int):
        super().__init__(width, height, layers)
        self.specialValues = {}
        self.simulated = True

    def step(self) -> None:
        if self.simulated:
            return super().step()
        return None
    
    def reset(self) -> None:
        self.simulated = True
        return super().reset()

    def __str__(self) -> str:
        return f'SimulatedBoard({self.getWidth()}, {self.getHeight()}, {self.getLayerCount()})'
    
    def __repr__(self) -> str:
        return f'<SimulatedBoard({self.getWidth()}, {self.getHeight()}, {self.getLayerCount()})>'
    
    def __del__(self) -> None:
        if self.python_delete_agents is not None:
            self.python_delete_agents()
        else:
            print("WARNING: You have not initialized your agents against the board! This might cause memory problems... Check: Agents.initialize_agents")
        super().__del__()