# Bugs

- [ ] When adding a new thing in a pos that is put of bounds, it still works... Should throw error!
- [ ] If you add the drawer after agents are added, there is an error (add all agents after startup)

# Features

- [ ] make the agents reset by board. This will allow multiple boards at the same time
- [ ] Figure out a way to parallelize boards. (IDK, probably it's something about the GIL)
- [ ] Add a list of objects of certain type (like colors)
- [ ] Use python exceptions. (Currently using c++ exceptions)
- [ ] Make more detailed exceptions

# Docs

- [ ] Actually make nice docs

# Build

- [ ] Figure out how tf to automize wheels on windows
- [ ] Make github actions that automatically make a new post
- [ ] Eventually upload to PyPi