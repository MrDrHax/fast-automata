from . import BaseClasses, Board, ClassTypes, Agents
from typing import Callable
import csv, timeit, itertools

class Tester(BaseClasses.IBaseAttachment):
    '''
    A testing class that will execute the board and print the results.

    Results will be stored as a csv file in the current directory, named results.csv.

    Results will include: run #, board.color_map_count, board.specialValues
    '''

    def __init__(self, data: dict[str, list[any]], boardSizes: list[ClassTypes.Pos], boardConstructor: Callable[[dict[str, any]], Board.SimulatedBoard], repetitions: int = 1, filename: str = "results.csv"):
        '''
        Make a new tester attachment.

        The data is what will get used to create the board, and will be added to the board's specialValues.

        Parameters:
            data (dict[str, any]): The data to use to create the board. Call the boardConstructor with every possible combination from data.
                - any (list): the list of data value
            boardSizes (list[ClassTypes.Pos]): The board sizes to use
            boardConstructor (Callable[[dict[str, any]], Board.SimulatedBoard]): The board constructor to use
            repetitions (int): The amount of times to repeat each board
        '''
        self.data = data
        self.repetitions = repetitions
        self.boardSizes = boardSizes
        self.boardConstructor = boardConstructor
        self.filename = filename

    def run(self):
        print("Starting test suite. Please do not stop the program until it finishes with the message 'Finished!'. \nSaves to results.csv take a while, and are the last step.")
        print("Planed stages: Initializing, Running, Saving")
        print(">>>>>>>>>> Stage: Initializing <<<<<<<<<<")
        # calculate amount of runs
        runs = 1
        totalRuns = 0

        for key, value in self.data.items():
            runs *= len(value)

        totalRuns = runs * self.repetitions

        print(f"To run:\n> Total runs: {totalRuns * len(self.boardSizes)}\n> Unique combinations: {runs * len(self.boardSizes)}\n> Dictionary combinations: {runs}\n> Repetitions: {self.repetitions}")

        headers = ["run", "steps", "time"]

        dummyData = {}

        for key in self.data.keys():
            dummyData[key] = self.data[key][0]

        dummyData["board_width"] = 1
        dummyData["board_height"] = 1

        dummyBoard = self.boardConstructor(dummyData)
        for key in dummyData.keys():
            headers.append(f"data.{key}")

        for key in dummyBoard.specialValues.keys():
            headers.append(f"specialValues.{key}")
        
        for key in dummyBoard.color_map_count.keys():
            headers.append(f"state.{key}")

        print(f"Headers: {headers}")

        # initialize csv
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

        dummyBoard = None

        # boards: list[Board.SimulatedBoard] = [] # TODO remove this and make it a single var. When the memory issue gets fixed.

        # start testing
        print(">>>>>>>>>> Stage: Running <<<<<<<<<<")
        timePerStep = 1
        for dimension in self.boardSizes:
            print(f"\n\n>>> Dimension: {dimension} (from {self.boardSizes})")

            step = 0

            for values in itertools.product(*self.data.values()):
                

                localData = dict(zip(self.data.keys(), values))
                localData["board_width"] = dimension.x
                localData["board_height"] = dimension.y

                board = self.boardConstructor(localData)

                for i in range(self.repetitions):
                    print(f"\rStep: {step * self.repetitions + 1 + i}/{runs * self.repetitions}. ETA: {round(runs * timePerStep * self.repetitions / 10) * 10} seconds", end="")
                    start = timeit.default_timer()
                    board.reset()

                    while board.simulated:
                        board.step()
                    
                    end = timeit.default_timer()

                    # TODO calculate data and add to csv
                    with open(self.filename, "a", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=headers)

                        # Add prefix to keys in board.specialValues
                        prefixed_specialValues = {f"specialValues.{k}": v for k, v in board.specialValues.items()}

                        # Add prefix to keys in board.color_map_count
                        prefixed_color_map_count = {f"state.{k}": v for k, v in board.color_map_count.items()}

                        # Add prefix to keys in localData
                        prefixed_localData = {f"data.{k}": v for k, v in localData.items()}

                        writer.writerow({
                            "run": step * self.repetitions + i,
                            "steps": board.step_count,
                            "time": end - start,
                            **prefixed_specialValues,
                            **prefixed_color_map_count,
                            **prefixed_localData
                        })

                    timePerStep = (timePerStep + (timeit.default_timer() - start)) / 2


                step += 1