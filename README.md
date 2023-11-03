# Fast-Automata

A very simple, easy to use cellular automata simulator.

It was built based on mesa. I hated that, so I decided to build this.

to get started:

(start a grid and move them right)
```py
from fastautomata import LocalDraw, Board, Agents, ClassTypes

class costomAgent(Agents.Agent):
    def step(self):
        self.next_pos = self.pos + ClassTypes.Pos(1, 0)

playBoard = Board.SimulatedBoard(50, 50, 1)

drawEngine = LocalDraw.LocalDraw(playBoard, 800, 800)

dude = costomAgent(ClassTypes.Pos(5,5), "Alive", playBoard)
dude2 = costomAgent(ClassTypes.Pos(10,10), "Alive", playBoard)

drawEngine.run()
```

> This is one of the first versions. i need to make an api plugin. I would also like to add gpu acceleration or something.

`python setup.py sdist bdist_wheel`