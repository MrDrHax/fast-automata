from fastautomata import LocalDraw, Board, Agents
from fastautomata.ClassTypes import Pos

playBoard = Board.SimulatedBoard(10, 10, 1) # layers cannot be < 1

class CostumeAgent(Agents.SimulatedAgent):
    '''My agent that runs the simulation'''
    def step(self):
        self.pos = self.pos + Pos(1, 0) # move the object one to the right (on the x axis)

drawEngine = LocalDraw.LocalDraw(playBoard, 800, 800)

Agents.initialize_agents(playBoard)

def generateCells(board: Board.SimulatedBoard): # Note: on_reset gives a reference to a board. 
    for y in range(board.getHeight()):
        CostumeAgent(board, Pos(0, y), "Alive")

playBoard.append_on_reset(generateCells)

drawEngine.run()