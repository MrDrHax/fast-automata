from . import LocalDraw, Board, Agents, ClassTypes
import logging, random

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

conditioners = {
    ("Dead", "Dead", "Dead"): "Dead",
    ("Dead", "Dead", "Alive"): "Alive",
    ("Dead", "Alive", "Dead"): "Dead",
    ("Dead", "Alive", "Alive"): "Alive",
    ("Alive", "Dead", "Dead"): "Alive",
    ("Alive", "Dead", "Alive"): "Dead",
    ("Alive", "Alive", "Dead"): "Alive",
    ("Alive", "Alive", "Alive"): "Dead",
}

class costomAgent(Agents.Agent):

    def __init__(self, pos: ClassTypes.Pos, state: str, board: Board.SimulatedBoard, layer: int = 0):
        super().__init__(pos, state, board, layer)
        self.times = 0

    def step(self):
        if self.pos.y == self._board.height - 1:
            return

        neighbors = self.get_neighbors(1, True)

        neighborsStates = (neighbors[0].state, neighbors[1].state, neighbors[2].state) # take the top 3 neighbors in order: top left, top, top right

        self.next_state = conditioners[neighborsStates]

playBoard = Board.SimulatedBoard(50, 50, 1)

drawEngine = LocalDraw.LocalDraw(playBoard, 800, 800)

def startAgents(board: Board.SimulatedBoard):
    for i in range(board.width):
        for j in range(board.height):
            if j == board.height - 1 and  random.random() < 0.1:
                costomAgent(ClassTypes.Pos(i, j), "Alive", board)
            else:
                costomAgent(ClassTypes.Pos(i, j), "Dead", board)

playBoard.on_reset.append(startAgents)

startAgents(playBoard)

drawEngine.run()