import pyglet as pyg
from pyglet.window import key
import pyglet.shapes as shapes
from pyglet import gl

from . import fastautomata_clib

from . import Board, ClassTypes, Agents

import logging

logger = logging.getLogger(__name__)

def other(thingy):
    pass

class LocalDraw():
    '''
    An attachable object that draws the board on a window.

    The following are important methods:
    - step: Make a step in the simulation
    - boardReset: Reset the board
    - run: Run the window

    You will probably need to only call the run method.

    Creates a special variable named "draw_framerate" in the board. Change this to change the framerate of the simulation.

    Controls:
    - N: Next step (one step)
    - R: Reset
    - P: Pause/Play
    '''

    def __init__(self, board: Board.SimulatedBoard, width: int, height: int, padding: int = 1):
        '''
        Initialize a window and attach itself to the board

        Parameters:
            board (Board.SimulatedBoard): The board to attach to
            width (int): The width of the window (in pixels)
            height (int): The height of the window (in pixels)
            padding (int): The padding between cells to make squares (in pixels)
        '''
        self.board = board
        self.padding = padding
        self.window = pyg.window.Window(width, height)
        self.cellSize = ClassTypes.Pos(width // board.getWidth(), height // board.getHeight())
        self.base_board = pyg.graphics.Batch()
        self.cells = [
            [
                shapes.Rectangle(
                    x       = i * self.cellSize.x + padding, 
                    y       = j * self.cellSize.y + padding, 
                    width   = self.cellSize.x - padding * 2, 
                    height  = self.cellSize.y - padding * 2, 
                    color   = (150, 150, 150), 
                    batch   = self.base_board
                )
                for j in range(board.getHeight())
            ] 
            for i in range(board.getWidth())
        ]

        self.window.push_handlers(self.on_key_press)

        self.layered_batch = [pyg.graphics.Batch() for _ in range(board.getLayerCount())]
        self.drawn_agents: dict[int, shapes.Rectangle] = {}
        #pyg.clock.schedule_interval(self.update, 1.0/60.0)

        self.board.append_on_add(self.add_agent)
        # self.board.on_add.append(other)
        self.board.append_on_delete(self.remove_agent)
        self.board.append_on_reset(self.reset)

        self.board.specialValues["draw_framerate"] = 0.5

        self.playing = False

        logger.info("LocalDraw initialized")
        logger.info(f"Board size: {board.getWidth()}x{board.getHeight()}")
        logger.info(f"Window size: {width}x{height}")
        logger.info("Press N to step")
        logger.info("Press R to reset")
        logger.info("Press p to pause/play")

    def draw(self):
        '''
        Draw the screen
        '''
        gl.glClearColor(255, 255, 255, 1)  # Set background color to white
        self.window.clear()
        self.base_board.draw()

        for batch in self.layered_batch:
            batch.draw()

    def step(self, dx = 0):
        '''
        Make a step in the simulation.

        Will draw itself after the step.

        Calls the step method of the board.
        '''
        # start = time.time()
        self.board.step()
        self.draw()
        # logger.debug(f"Step took {((time.time() - start) / 1000):.4f}ms")

    def add_agent(self, agent: fastautomata_clib.BaseAgent):
        '''
        Add an agent to the board.

        Will get called automatically by the agent.
        '''

        newDrawnAgent = shapes.Rectangle(
            x       = agent.pos.x * self.cellSize.x + self.padding, 
            y       = agent.pos.y * self.cellSize.y + self.padding, 
            width   = self.cellSize.x - self.padding * 2, 
            height  = self.cellSize.y - self.padding * 2, 
            color   = self.board.color_map[agent.state], 
            batch   = self.layered_batch[agent.getLayer()]
        )

        self.drawn_agents[agent.getId()] = newDrawnAgent

        if isinstance(agent, fastautomata_clib.Agent):
            # logger.debug(f"Agent {agent.getId()} added")
            agent.append_on_update(self.update_agent)

    def on_key_press(self, symbol, modifiers):
        '''
        The event handler for key presses.
        '''

        if symbol == key.N:
            self.step()  # Call step method
        elif symbol == key.R:
            self.boardReset()  # Call boardReset method
        elif symbol == key.P:
            if self.playing:
                pyg.clock.unschedule(self.step)
                self.playing = False
            else:
                pyg.clock.schedule_interval(self.step, self.board.specialValues['draw_framerate']) # Call step method every 0.5 seconds
                self.playing = True

    def update_agent(self, agent: Agents.SimulatedAgent):
        '''
        Called by an agent when it's updated. 
        '''

        self.drawn_agents[agent.getId()].color = self.board.color_map[agent.state]
        self.drawn_agents[agent.getId()].x = agent.pos.x * self.cellSize.x
        self.drawn_agents[agent.getId()].y = agent.pos.y * self.cellSize.y

    def remove_agent(self, agent: fastautomata_clib.BaseAgent):
        '''
        Gets called when agent kills itself.
        '''

        self.drawn_agents[agent.getId()].delete()
        self.drawn_agents.pop(agent.getId())

    def reset(self, board: Board.SimulatedBoard):
        '''
        Resets the board.

        Will get called automatically by the board.
        '''

        for key in self.drawn_agents:
            self.drawn_agents[key].delete()
        
        self.drawn_agents = {}

        self.draw()

    def boardReset(self):
        '''
        Resets the board.

        Calls the Reset method of the board.
        '''

        self.board.reset()

    def run(self):
        '''
        The default run method.

        Use this to let pyglet take control of the app
        '''

        @self.window.event
        def on_draw():
            self.draw()

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.on_key_press(symbol, modifiers)

        pyg.app.run()
