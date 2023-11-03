from . import Agents, ClassTypes
from enum import Enum
from pydantic import BaseModel
from typing import Callable

import logging, time

import concurrent.futures

logger = logging.getLogger(__name__)

class Collision(BaseModel):
    '''A collision between two layers'''

    layer_id: int
    '''The layer that the collision is referring to'''

    collision_type: ClassTypes.CollisionType
    '''The type of collision with the other layer'''

class CollisionList(BaseModel):
    '''A list of collisions between a layer and others'''

    collisions: list[Collision]
    '''The list of collisions that will be used to determine what happens when two layers collide'''

class CollisionMap(BaseModel):
    '''A map of collisions between layers'''

    collision_map: dict[int, CollisionList]
    '''The collisions map that will be used to determine what happens when two layers collide'''

class SimulatedBoard():
    '''A board that is simulated and can be used to test agents'''

    width: int
    height: int

    layers: list[list['Agents.BaseAgent' or None]]

    layer_collisions: CollisionMap
    '''The collisions map that will be used to determine what happens when two layers collide'''

    agents: list['Agents.Agent']
    '''The updatable agents that are currently on the board'''

    step_count: int
    '''The number of steps that have been taken'''

    step_instructions: list[Callable[['SimulatedBoard'], None]]
    '''The instructions that will get called each update. They are not guaranteed to be in order.'''

    color_map: dict[str, tuple[int, int, int]]
    '''The color map for the board. It is a dictionary with the state as the key and the color (in r,g,b format) as the value.'''

    on_reset: list[Callable[['SimulatedBoard'], None]]
    '''The functions that will be called when the board is reset'''

    on_add: list[Callable[[Agents.BaseAgent], None]]
    '''When a cell is added this gets called with the agent that was added'''

    on_delete: list[Callable[[Agents.BaseAgent], None]]
    '''When a cell is deleted this gets called with the agent that was deleted'''

    def __init__(self, width: int, height: int, layers: int, on_reset: list[Callable[['SimulatedBoard'], None]] = []):
        self.width = width
        self.height = height

        self.layers = [[None for _ in range(width * height)] for _ in range(layers)]

        self.step_instructions = [SimulatedBoard.update_agents, SimulatedBoard.update_agents_end]

        self.agents = []

        self.color_map = {"Dead": (50,50,50), "Alive": (25,255,64)} # default dead or alive

        self.on_reset = on_reset

        self.on_add = []
        self.on_delete = []

        self.step_count = 0

    def reset(self):
        self.layers = [[None for _ in range(self.width * self.height)] for _ in range(len(self.layers))]

        self.agents = []

        self.step_count = 0

        for callable in self.on_reset:
            callable(self)

    def step(self):
        timeMS = 0
        for individual_step in self.step_instructions:
            start = time.time()
            individual_step(self)

            msTook = (time.time() - start) * 1000
            timeMS += msTook
            logger.debug(f"Sub-Step {individual_step.__name__} took {msTook} ms.")
        logger.debug(f"Step {self.step_count} took {msTook} ms.")

        self.step_count += 1

    def agent_add(self, agent: Agents.BaseAgent):
        self.layers[agent.layer][agent.pos.toIndex(self.width)] = agent

        if isinstance(agent, Agents.Agent):
            self.agents.append(agent)

        for callable in self.on_add:
            callable(agent)

    def agent_remove(self, agent: Agents.BaseAgent | Agents.Agent):
        self.layers[agent.layer][agent.pos.toIndex(self.width)] = None

        if isinstance(agent, Agents.Agent):
            self.agents.remove(agent)

        for callable in self.on_delete:
            callable(agent)

    def agent_get(self, pos: ClassTypes.Pos, layer: int|None = None, wrap: bool = False) -> Agents.BaseAgent | None:
        if pos.x < 0 or pos.x >= self.width or pos.y < 0 or pos.y >= self.height:
            if wrap:
                pos = ClassTypes.Pos(pos.x % self.width, pos.y % self.height)
            else:
                return None

        if layer is not None:
            return self.layers[layer][pos.toIndex(self.width)]
        else:
            return self.layers[0][pos.toIndex(self.width)]

    @staticmethod
    def update_agents(board: 'SimulatedBoard'):
        # TODO: make parallel and on gpu
        for agent in board.agents:
            agent.step()

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     executor.map(lambda agent: agent.step(), board.agents)

    @staticmethod
    def update_agents_end(board: 'SimulatedBoard'):
        # TODO: make parallel and on gpu
        for agent in board.agents:
            agent.step_end()

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     executor.map(lambda agent: agent.step_end(), board.agents)