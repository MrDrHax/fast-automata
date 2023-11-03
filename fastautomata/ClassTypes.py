from enum import Enum

class Pos():
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return (self.x, self.y)
    
    def __repr__(self):
        return f"pos({self.x}, {self.y})"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Pos):
            return self.x == o.x and self.y == o.y
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def toIndex(self, width: int) -> int:
        return self.y * width + self.x
    
    # add and subtract 
    def __add__(self, o: 'Pos') -> 'Pos':
        return Pos(self.x + o.x, self.y + o.y)
    
    def __sub__(self, o: 'Pos') -> 'Pos':
        return Pos(self.x - o.x, self.y - o.y)
    
    # addequal and subequal
    def __iadd__(self, o: 'Pos') -> 'Pos':
        self.x += o.x
        self.y += o.y
        return self
    
    def __isub__(self, o: 'Pos') -> 'Pos':
        self.x -= o.x
        self.y -= o.y
        return self
    
class CollisionType(Enum):
    '''The type of collision with the other layer'''

    NONE = 0 
    '''no collision, gets ignored'''

    AGENT = 1 
    '''collision with other agent, they can coexist'''

    WALL = 2 
    '''collision with wall, agent cannot move there (collider)'''

    INFO = 3 
    '''collision with info, agent can move there with no problems (trigger)'''
