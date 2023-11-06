'''
A wrapper for the agents in the simulation
'''

from . import fastautomata_clib
from pydantic import BaseModel
from .Board import SimulatedBoard as Board
from .ClassTypes import Pos, PosModel

import logging

logger = logging.getLogger(__name__)

simulatedAgentList: list[fastautomata_clib.Agent] = []
staticAgentList: list[fastautomata_clib.BaseAgent] = []

def initialize_agents(board: Board):
    '''
    sets the board reset function to resetAgents
    '''
    board.append_on_reset(resetAgents)

def resetAgents(board: Board):
    '''
    Clears the agent lists
    '''
    simulatedAgentList.clear()
    staticAgentList.clear()


class SimulatedAgent(fastautomata_clib.Agent):
    '''
    A pythonic wrapper for the agents in the simulation
    '''

    def __init__(self, board: Board, pos: Pos, state: int, layer: int = 0, allowOverriding: bool = False):
        super().__init__(board, pos, state, layer, allowOverriding)
        simulatedAgentList.append(self)

    def kill(self):
        super().kill()
        simulatedAgentList.remove(self)

    def step(self) -> None:
        logger.error("You have not overriden the simulated agent!!!!")

    def __str__(self) -> str:
        return super().__str__()
    
    def __repr__(self) -> str:
        return super().__repr__()
    
class StaticAgent(fastautomata_clib.BaseAgent):
    '''
    A pythonic wrapper for the agents in the simulation
    '''
    def __init__(self, board: Board, pos: Pos, state: int, layer: int = 0, allowOverriding: bool = False):
        super().__init__(board, pos, state, layer, allowOverriding)
        staticAgentList.append(self)

    def kill(self):
        super().kill()
        staticAgentList.remove(self)

    def __str__(self) -> str:
        return f"StaticAgent at {self.pos}"
    
    def __repr__(self) -> str:
        return f"<StaticAgent at {self.pos}, state: {self.state}>"



class SimplifiedAgentModel(BaseModel):
    id: int
    pos: PosModel
    state: str
    layer: int

    def __init__(self, agent: fastautomata_clib.BaseAgent):
        self.id = agent.getId()
        self.pos = PosModel(x=agent.pos.x, y=agent.pos.y)
        self.state = agent.state
        self.layer = agent.getLayer

class AgentsModel(BaseModel):
    '''
    A wrapper for the agents in the simulation

    Used to export to json
    '''
    simulated: list[SimplifiedAgentModel]
    static: list[SimplifiedAgentModel]

    total: int

    def __init__(self):
        global simulatedAgentList, staticAgentList
        self.total = len(simulatedAgentList) + len(staticAgentList)
        self.simulated = simulatedAgentList
        self.static = staticAgentList