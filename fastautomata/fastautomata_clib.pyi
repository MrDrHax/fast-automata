from typing import Any, Callable, ClassVar, Dict, List

from typing import overload
NONE: CollisionType
SOLID: CollisionType
TRIGGER: CollisionType

class Agent(BaseAgent):
    on_update: List[Callable[[Agent],None]]
    pos: Pos
    state: str
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, board: SimulatedBoard, pos: Pos, state: str, layer: int = 0, allowOverriding: bool = False) -> None: ...
    def append_on_update(self, toAppend: Callable[[Agent],None]) -> None: ...
    '''Add a call to toAppend to the on_update list'''
    def get_neighbors(self, radius: int, wrap: bool = False, layer: int = -1) -> List[BaseAgent]: ...
    '''
    Returns a list of agents within a radius of the agent. 
    If wrap is true, the board will wrap around the edges. 
    If layer is -1, it will consider itself.
    '''
    def step(self) -> None: ...
    '''
    Called by the board every step.

    MUST BE OVERRIDDEN
    '''
    def step_end(self) -> None: ...
    '''
    The final step called by the board. All changes get applied.
    '''

class BaseAgent:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, board: SimulatedBoard, pos: Pos, state: str, layer: int = 0, allowOverriding: bool = False) -> None: ...
    def checkCollisions(self, type: CollisionType, searchIn: Pos) -> bool: ...
    '''
    A wrapper function that calls the board's getCollisions function. Used the Agent's layer.
    '''
    def getId(self) -> int: ...
    '''
    readonly ID
    '''
    def getLayer(self) -> int: ...
    '''
    read the layer.
    '''
    def kill(self) -> None: ...
    '''
    Remove the agent from the simulation. Removes agent from board and deleted the agent's pointer.
    '''
    @property
    def board(self) -> SimulatedBoard: ...
    '''
    readonly board pointer
    '''
    @property
    def pos(self) -> Any: ...
    '''
    Get and set the position of the agent.

    The position will set a temporary position_next, and will get updated on step_end.
    '''
    @property
    def state(self) -> str: ...
    '''
    Get and set the state of the agent.

    The state will set a temporary state_next, and will get updated on step_end.
    '''

class CollisionList:
    '''
    Used to store a collision from one place to another.
    '''
    def __init__(self) -> None: ...
    def addCollision(self, type: CollisionType, layer: int) -> None: ...
    '''
    Add a new collision to the list

    Parameters:
        type: The type of collision. Must be a CollisionType, this will define the way collisions work.
        layer: The layer to collide with. If the current layer hits that other layer, how will the collision work?
    '''
    def getCollision(self, layer: int) -> CollisionType: ...
    '''
    Get the collision type with another layer.
    '''

class CollisionMap:
    '''
    A map of all the collisions between layers.
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, length: int) -> None: ...
    '''
    Start with length amount of layers.
    '''
    @overload
    def __init__(self, arg0: CollisionList, arg1: int) -> None: ...
    '''
    Idk what this does, but it will get called automatically from c++, you are not supposed to call this.
    '''
    def addCollision(self, collision: CollisionType, layer_start: int, layer_end: int) -> None: ...
    '''
    Add a new collision to the map.

    Parameters:
        collision: The type of collision. Must be a CollisionType, this will define the way collisions work.
        layer_start: The layer from which the collision will get rendered from.
        layer_end: The layer to which the collision will get rendered to.
    '''
    def getCollision(self, layer_start: int, layer_end: int) -> CollisionType: ...
    '''
    Get the collision type between two layers.

    Parameters:
        layer_start: The layer from which the collision will get rendered from.
        layer_end: The layer to which the collision will get rendered to.
    '''

class CollisionType:
    __members__: ClassVar[dict] = ...  # read-only
    NONE: ClassVar[CollisionType] = ...
    '''Ignore collision. It will also returned by getCollisions()'''
    SOLID: ClassVar[CollisionType] = ...
    '''Solid collision. It will also returned by getCollisions(). If a collision is solid, a simulatedagent will not get made there or move. '''
    TRIGGER: ClassVar[CollisionType] = ...
    '''Trigger collision. It will also returned by getCollisions(). If a collision is a trigger, a simulatedagent can move there. '''
    __entries: ClassVar[dict] = ...
    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class Pos:
    x: int
    '''The x position of the position'''
    y: int
    '''The y position of the position'''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, x: int, y: int) -> None: ...
    def copy(self) -> Pos: ...
    def magnitude(self) -> float: ...
    def normalize(self) -> Pos: ...
    def toIndex(self, width: int) -> int: ...
    '''Convert the x,y coordinates to an array index.'''
    def toString(self) -> str: ...
    def __add__(self, other: Pos) -> Pos: ...
    def __div__(self, other: Pos) -> Pos: ...
    def __eq__(self, other: Pos) -> bool: ...
    def __floordiv__(self, other: Pos) -> Pos: ...
    def __gt__(self, other: Pos) -> bool: ...
    def __hash__(self, other: int) -> int: ...
    def __iadd__(self, other: Pos) -> Pos: ...
    def __idiv__(self, other: Pos) -> Pos: ...
    def __ifloordiv__(self, other: Pos) -> Pos: ...
    def __imod__(self, other: Pos) -> Pos: ...
    def __imul__(self, other: Pos) -> Pos: ...
    def __isub__(self, other: Pos) -> Pos: ...
    def __lt__(self, other: Pos) -> bool: ...
    def __mod__(self, other: Pos) -> Pos: ...
    def __mul__(self, other: Pos) -> Pos: ...
    def __ne__(self, other: Pos) -> bool: ...
    def __sub__(self, other: Pos) -> Pos: ...

class SimulatedBoard:
    color_map_count: Dict[str,int]
    '''
    Keeps track of the agents on the board

    readonly!!!
    '''
    color_map: Dict[str,List[int[3]]]
    '''
    A map of all the colors. The key is the cell type, and the value is rgb colors in list format.
    
    WARNING: Do not use .append() to add colors. Use .addColor() instead.
    '''
    layer_collisions: CollisionMap
    '''A map of all the collisions between layers.'''
    on_add: list[Callable[[BaseAgent],None]]
    '''
    A list of functions that will get called when an agent gets added.
    
    WARNING: Using .append() will not work. Use .append_on_add() instead.
    '''
    on_delete: list[Callable[[BaseAgent],None]]
    '''
    A list of functions that will get called when an agent gets deleted.

    WARNING: Using .append() will not work. Use .append_on_delete() instead.
    '''
    on_reset: list[Callable[[SimulatedBoard],None]]
    '''
    A list of functions that will get called when the board gets reset.

    WARNING: Using .append() will not work. Use .append_on_reset() instead.
    '''
    step_instructions: List[Callable[[SimulatedBoard],None]]
    '''
    A list of functions that will get called when the board steps.

    By default it will call the step() and step_end() method of all the agents.

    WARNING: Using .append() will not work. Use .step_instructions_add() instead.

    To reset use step_instructions_flush
    '''
    def __init__(self, width: int, height: int, layers: int) -> None: ...
    '''
    Create a new board with width, height, and layers.
    '''
    def addColor(self, key: str, value: List[int[3]]) -> None: ...
    '''
    Add a new color to the color_map.
    '''
    def agent_add(self, agent: BaseAgent, allowOverrides: bool = False) -> None: ...
    '''
    Add a new agent to the board. 
    
    You should't call this directly, the agent's constructor calls it already.

    Parameters:
        agent: The agent to add.
        allowOverrides: If true, the agent will replace the other agent in the same pos.
    '''

    def agent_get(self, pos: Pos, layer:int = 1, wrap: bool = False) -> Any: ...
    '''
    Get an agent from the board. 

    parameters:
        pos: The position to get the agent from.
        layer: The layer to get the agent from.
        wrap: If true, the board will wrap around to the other side of the board.
    '''

    def agent_move(self, agent: BaseAgent, posPrev: Pos, posNew: Pos) -> None: ...
    '''
    Move an agent from one position to another.

    WARNING: This will not check for collisions. Use the agent's built in method.

    An agent that is moved by changing it's pos will call this function on step_end.
    '''

    def agent_move_layer(self, agent: BaseAgent, layerNew: int) -> None: ...
    '''
    Change an agent's layer.

    Not recommended to use. But you do you. 
    '''

    def agent_remove(self, arg0) -> None: ...
    '''
    Remove an agent from the board.

    You should't call this directly, the agent's kill() method calls it already, but that's just a wrapper.
    '''

    def append_on_add(self, func: Callable[[BaseAgent], None]) -> None: ...
    '''
    Append a new function to the on_add list.
    '''

    def append_on_delete(self, func: Callable[[BaseAgent], None]) -> None: ...
    '''
    Append a new function to the on_delete list.
    '''

    def append_on_reset(self, func: Callable[[SimulatedBoard],None]) -> None: ...
    '''
    Append a new function to the on_reset list.
    '''

    def getCollisions(self, pos: Pos, layer:int = 0, includeSelf: bool = False) -> Dict[int, tuple[CollisionType, BaseAgent|None]]: ...
    '''
    Returns a dictionary of all the collisions at a position.

    Will always return the full list of collisions, even if the collision is NONE.

    Parameters:
        pos: The position to check for collisions.
        layer: The layer to check for collisions.
        includeSelf: If true, it will count collision with self.
    '''

    def getHeight(self) -> int: ...
    '''
    Return the defined height of the board.
    '''

    def getLayerCount(self) -> int: ...
    '''
    Return the defined layer count of the board.
    '''

    @staticmethod
    def getRandomColor() -> List[int[3]]: ...
    '''
    Gets a random color. Literally nothing more to it.
    '''

    def getWidth(self) -> int: ...
    '''
    Return the defined width of the board.
    '''

    def reset(self) -> None: ...
    '''
    Reset the board. Calls all the functions in the on_reset list.
    Deletes all the agents.
    '''

    def step(self) -> None: ...
    '''
    Make a board step. Calls all the functions in the step_instructions list.

    By default update_agents and update_agents_end are added to step_instructions.
    '''

    def updateColor(self, arg0: str, arg1: str) -> None: ...
    '''
    Update the color of a cell type.

    used to get count of cell types.

    Gets called automatically by a cell.
    '''

    @staticmethod
    def update_agents(self) -> None: ...
    '''
    Update all the agents. Calls the step() method of all the agents.
    '''

    @staticmethod
    def update_agents_end(self) -> None: ...
    '''
    Update all the agents. Calls the step_end() method of all the agents.
    '''
