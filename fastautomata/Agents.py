import ClassTypes
import Board
from typing import Callable

nextID = 0

class BaseAgent():
    pos: ClassTypes.Pos
    state: str
    next_state: str | None
    next_pos: ClassTypes.Pos | None
    layer: int

    id: int

    _board: 'Board.SimulatedBoard' or None = None #: Board.SimulatedBoard

    def __init__(self, pos: ClassTypes.Pos, state: str, board: 'Board.SimulatedBoard', layer: int = 0):
        self.pos = pos
        self.state = state
        self.next_state = None
        self.layer = layer

        self._board = board

        global nextID
        self.id = nextID
        nextID += 1

    def __repr__(self) -> str:
        return f"Agent({self.pos}, {self.state}, {self.layer})"
    
    def kill(self):
        self._board.agents.remove(self)


class Agent(BaseAgent):
    '''
    An agent that can move around the board.

    gets updated each frame.

    Registers automatically to the board it is added to.
    '''
    on_update: list[Callable[['Agent'], None]]

    def __init__(self, pos: ClassTypes.Pos, state: str, board: 'Board.SimulatedBoard', layer: int = 0):
        super().__init__(pos, state, board, layer)

        self.next_pos = None
        self.next_state = None

        self.on_update = []
        self._board.agent_add(self)

    
    def step(self):
        pass

    def step_end(self):
        updated = False

        # update state
        if self.next_state is not None:
            self.state = self.next_state
            self.next_state = None
            updated = True

        # update position
        if self.next_pos is not None:
            self.pos = self.next_pos
            self.next_pos = None
            updated = True

        # call on_update
        if updated:
            for callable in self.on_update:
                callable(self)

    def get_neighbors(self, radios: int = 1, wrap: bool = False) -> list['Agent']:
        toReturn = []

        for j in range(self.pos.y + radios, self.pos.y - radios - 1, -1):
            for i in range(self.pos.x - radios, self.pos.x + radios + 1):
                toReturn.append(self.get_agent_in_pos(ClassTypes.Pos(i, j), wrap))

        return toReturn

    def get_agent_in_pos(self, pos: ClassTypes.Pos, wrap: bool = False) -> BaseAgent | None:
        return self._board.agent_get(pos, self.layer, wrap)

    def move(self, relative_pos: ClassTypes.Pos) -> bool:
        calculatedPos = self.pos + relative_pos

        if ClassTypes.CollisionType.WALL in self.checkCollisions(calculatedPos):
            print(f"Wall collision {self.pos} -> {calculatedPos}")
            return False

        self.next_pos = calculatedPos
        self._board.layers[self.layer][self.pos.toIndex(self._board.width)] = self

    def checkCollisions(self, pos: ClassTypes.Pos) -> list[ClassTypes.CollisionType]:
        '''Test for collisions at a position'''
        # TODO move this to board. Make the call to board checkCollisions, and send the agent's parameters

        collisions = self._board.layer_collisions.collision_map[self.layer]

        toReturn: list[ClassTypes.CollisionType] = []

        index = pos.toIndex(self._board.width)

        for collision in collisions.collisions:
            agentInPos = self._board.layers[collision.layer][index]
            if agentInPos is not None:
                toReturn.append(collision.collision_type)

        return toReturn

class StaticAgent(BaseAgent):
    '''
    An agent that does not get updated.

    Can be used for walls, points, etc.
    '''
    pass