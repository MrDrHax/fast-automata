from fastautomata import fastautomata_clib

# create a board and test it
board = fastautomata_clib.SimulatedBoard(10, 10, 1)

# Test that it actually worked
print(board.getWidth())