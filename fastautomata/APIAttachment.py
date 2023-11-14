from .BaseClasses import IControlledAttachment
import fastapi, uvicorn
from . import Board, Agents, ClassTypes

class API(IControlledAttachment):
    def __init__(self, board: Board.SimulatedBoard) -> None:
        router = fastapi.APIRouter()

        router.add_api_route("/step", self.step, methods=["POST"])
        router.add_api_route("/reset", self.boardReset, methods=["POST"])
        router.add_api_route("/setVar", self.setVar, methods=["POST"])

        self.router = router
        self.board = board

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        self.app = fastapi.FastAPI()
        self.app.include_router(self.router)
        uvicorn.run(self.app, host=host, port=port)

    def setVar(self, varName: str, varValue: any):
        self.board.specialValues[varName] = varValue

    def boardReset(self):
        self.board.reset()

        return self.buildModel()
    
    def step(self):
        self.board.step()

        return self.buildModel()
    
    def buildModel(self):
        return {
            "board": self.board.buildModel(),
            "agents": Agents.AgentsModel(),
            "values": self.board.specialValues,
            "summary": self.board.color_map_count,
        }