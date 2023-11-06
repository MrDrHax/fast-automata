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

Install: `pip install git+https://github.com/MrDrHax/fast-automata.git`

> NOTE: you might need to have cmake and pybind11 installed. Idk

# Quick Docs

## Getting started

Fastautomata depends on 3 parts:

- Board
- Agents
- Interfacing agent

To import the basic utils of fastautomata use:

```py
from fastautomata import LocalDraw, Board, Agents
from fastautomata.ClassTypes import Pos
```

This will import most of the necessary objects.

### Simulated Board

To get started every simulation required a SimulatedBoard. to create one use:

```py
playBoard = Board.SimulatedBoard(10, 10, 1) # layers cannot be < 1
```

Once you have your board, you might want to create a costume SimulatedAgent. 

FastAutomata has 2 types of agents: Static and Simulated.

### Static Agents

Static agents work as walls or objects. They will be drawn, but no actions will be taken. Once created you will not be able to move them or edit them (the position).

You can inherit from a static agent to make costume functionality (such as define paths).

### Simulated Agents

Simulated agents have the additional ability to get stepped through. They usually go through 2 steps: step() and step_end()

You can define how the cell should behave by overriding the step() and step_end(), although in most cases step_end() should take care of everything.

To accomplish this, make your own class that inherits from the SimulatedAgent:

```py
class CostumeAgent(Agents.SimulatedAgent):
    '''My agent that runs the simulation'''
    def step(self):
        self.pos = self.pos + Pos(1, 0) # move the object one to the right (on the x axis)
```

> Note: By editing the state or pos of an object, you are actually editing a buffer called state_next and pos_next. The actual transition and update of the object will occur on step_end(). Feel free to update pos as many times as necessary. 

### Attaching interfaces

To attach an interface to a board, create a new interface and connect it to the board:

```py
drawEngine = LocalDraw.LocalDraw(playBoard, 800, 800)
```

LocalDraw is an agent that displays a board locally. It uses pyglet as a backend.

Any agent should attach itself to a board by using it's hooks. No further config should be necessary.

### Making a generator

To set the starting position of all your cells, you can create a function that will initialize all the necessary cells on the board. This si specially useful for on_reset calls.

```py
def generateCells(board: Board.SimulatedBoard): # Note: on_reset gives a reference to a board. 
    for y in range(board.getHeight()):
        CostumeAgent(board, Pos(0, y), "Alive")
```

This function will generate a row of cells with a `x` pos of 0, and a `y` pos of `y` (one for each step).

To attach the function use:

```py
playBoard.append_on_reset(generateCells)
```

Finally, call the function once to start it off (might get removed on the future, I'm planning on calling reset automatically when the first iteration is done)

```py
generateCells(playBoard)
```

### Running the simulator

As described previously, an interface will attach itself to a board. You can manually call the board and update agents, but interfaces do this for you. To run an interface, use interface.run():

```py
drawEngine.run()
```

### Summary

In the end, your code should look like this:

```py
from fastautomata import LocalDraw, Board, Agents
from fastautomata.ClassTypes import Pos

playBoard = Board.SimulatedBoard(10, 10, 1) # layers cannot be < 1

class CostumeAgent(Agents.SimulatedAgent):
    '''My agent that runs the simulation'''
    def step(self):
        self.pos = self.pos + Pos(1, 0) # move the object one to the right (on the x axis)

drawEngine = LocalDraw.LocalDraw(playBoard, 800, 800)

def generateCells(board: Board.SimulatedBoard): # Note: on_reset gives a reference to a board. 
    for y in range(board.getHeight()):
        CostumeAgent(board, Pos(0, y), "Alive")

playBoard.append_on_reset(generateCells)

generateCells(playBoard)

drawEngine.run()
```

That's it! 

After you have this file, you should see a screen of a green line.

Try pressing p on your keyboard to start the simulation.

## More in depth

### Colors

To make your own costume states, you can use the `addColor()` method of SimulatedBoard.

By default, 3 states exist: Alive, Dead and None.

If you use a string that is not defined, a new random color will get added. A warning will get shown.

### Layers

Layers define a way to add multiple objects to a single pos. 

By default, layers will not collide with other layers, but you can change this interaction by adding collisions. To add a collision use: `playBoard.layer_collisions.addCollision()`

### Collisions

If you try to change the pos of an object, and it contains a collision, the object will not get moved to that position.

### fastautomata_clib

Some stuff was not added to a pythonic way of working. Use Clib if you don't find something. Sorry, working on fixing it.

