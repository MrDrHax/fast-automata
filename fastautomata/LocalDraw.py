import pyglet as pyg
from pyglet.window import key
import pyglet.shapes as shapes
from pyglet import gl
import Board
import ClassTypes
import Agents

import logging

logger = logging.getLogger(__name__)

class LocalDraw():
    def __init__(self, board: Board.SimulatedBoard, width: int, height: int, padding: int = 1):
        self.board = board
        self.padding = padding
        self.window = pyg.window.Window(width, height)
        self.cellSize = ClassTypes.Pos(width / board.width, height / board.height)
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
                for j in range(board.height)
            ] 
            for i in range(board.width)
        ]

        self.window.push_handlers(self.on_key_press)

        self.layered_batch = [pyg.graphics.Batch() for _ in range(len(board.layers))]
        self.drawn_agents: dict[int, shapes.Rectangle] = {}
        #pyg.clock.schedule_interval(self.update, 1.0/60.0)

        self.board.on_add.append(self.add_agent)
        self.board.on_delete.append(self.remove_agent)
        self.board.on_reset.append(self.reset)

        self.playing = False

        logger.info("LocalDraw initialized")
        logger.info(f"Board size: {board.width}x{board.height}")
        logger.info(f"Window size: {width}x{height}")
        logger.info("Press N to step")
        logger.info("Press R to reset")
        logger.info("Press p to pause/play")

    def draw(self):
        gl.glClearColor(255, 255, 255, 1)  # Set background color to white
        self.window.clear()
        self.base_board.draw()

        for batch in self.layered_batch:
            batch.draw()

    def step(self, dt):
        self.board.step()
        self.draw()

    def add_agent(self, agent: Agents.BaseAgent):
        newDrawnAgent = shapes.Rectangle(
            x       = agent.pos.x * self.cellSize.x + self.padding, 
            y       = agent.pos.y * self.cellSize.y + self.padding, 
            width   = self.cellSize.x - self.padding * 2, 
            height  = self.cellSize.y - self.padding * 2, 
            color   = self.board.color_map[agent.state], 
            batch   = self.layered_batch[agent.layer]
        )

        self.drawn_agents[agent.id] = newDrawnAgent

        if isinstance(agent, Agents.Agent):
            agent.on_update.append(self.update_agent)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.N:
            self.step(0)  # Call step method
        elif symbol == key.R:
            self.boardReaset()  # Call boardReset method
        elif symbol == key.P:
            if self.playing:
                pyg.clock.unschedule(self.step)
                self.playing = False
            else:
                pyg.clock.schedule_interval(self.step, 0.5) # Call step method every 0.5 seconds
                self.playing = True

    def update_agent(self, agent: Agents.Agent):
        self.drawn_agents[agent.id].color = self.board.color_map[agent.state]
        self.drawn_agents[agent.id].x = agent.pos.x * self.cellSize.x
        self.drawn_agents[agent.id].y = agent.pos.y * self.cellSize.y

    def remove_agent(self, agent: Agents.BaseAgent):
        self.drawn_agents[agent.id].delete()
        self.drawn_agents.pop(agent.id)

    def reset(self, board: Board.SimulatedBoard):
        for key in self.drawn_agents:
            self.drawn_agents[key].delete()
        
        self.drawn_agents = {}

        self.draw()

    def boardReaset(self):
        self.board.reset()

    def run(self):
        @self.window.event
        def on_draw():
            self.draw()

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.on_key_press(symbol, modifiers)

        pyg.app.run()


# Usage:
# board = Board.Board(40, 30)
# draw = LocalDraw(board)
# draw.run()

# n > next step 
# r > reset