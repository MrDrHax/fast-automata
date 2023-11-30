from .BaseClasses import IControlledAttachment
import fastapi, uvicorn
from . import Board, Agents, ClassTypes
from pydantic import BaseModel
from typing import Any
from pydantic import BaseModel
from typing import Any
from . import Agents, Board

class API(IControlledAttachment):
    router: fastapi.APIRouter
    def __init__(self, board: Board.SimulatedBoard) -> None:
        router = fastapi.APIRouter()

        router.add_api_route("/step", self.step, methods=["POST"])
        router.add_api_route("/reset", self.boardReset, methods=["POST"])
        router.add_api_route("/setVar", self.setVar, methods=["POST"])
        router.add_api_route("/state", self.getCurrentState, methods=["GET"])

        self.router = router
        self.board = board

    def run(self, reset: bool = True, host: str = "0.0.0.0", port: int = 8000) -> None:
        self.app = fastapi.FastAPI()
        self.app.include_router(self.router)

        if reset:
            self.board.reset()

        uvicorn.run(self.app, host=host, port=port)

    def setVar(self, varName: str, varValue: Any):
        self.board.specialValues[varName] = varValue

    def getCurrentState(self) -> 'BoardModel':
        return self.buildModel()

    def boardReset(self) -> 'BoardModel':
        self.board.reset()

        return self.buildModel()
    
    def step(self) -> 'BoardModel':
        self.board.step()

        return self.buildModel()
    

    def buildModel(self) -> 'BoardModel':
        return BoardModel.makeNew(self.board)
    
class BoardModel(BaseModel):
    board: dict[str, tuple[int, int, int]]
    agents: Agents.AgentsModel
    values: dict[str, Any]
    summary: dict[str, int]
    step_count: int = 0

    # def __init__(self, board: Board.SimulatedBoard) -> None:

    @staticmethod
    def makeNew(board: Board.SimulatedBoard) -> 'BoardModel':
        self = BoardModel(
            board       = board.color_map,
            agents      = Agents.AgentsModel.makeNew(),
            values      = board.specialValues,
            summary     = board.color_map_count,
            step_count  = board.step_count
        )

        return self

    