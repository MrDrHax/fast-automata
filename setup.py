from setuptools import setup, find_packages

setup(
    name="fast-automata",
    version="0.2",
    packages=find_packages(),
    author="Alejandro Fernandez",
    author_email="alexfh2001@gmail.com",
    description="A 'fast' library for cellular automata simulations. I was just done with mesa and it's confusing/restrictive api.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MrDrHax/fast-automata",
    install_requires=["pyglet", "pydantic"],
    python_requires='>=3.10',
    license="GPLv3",
)