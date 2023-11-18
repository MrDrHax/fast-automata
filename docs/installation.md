# How to install and use fastautomata

In this doc, you will be able to install and configure fast automata. Please consider that fastautomata is currently on alpha... and installation can be pretty iffy.

- [How to install and use fastautomata](#how-to-install-and-use-fastautomata)
- [Windows](#windows)
  - [Install dependencies](#install-dependencies)
  - [Compile](#compile)
  - [Install](#install)
- [Linux](#linux)
  - [Install dependencies](#install-dependencies-1)
  - [Compile](#compile-1)
  - [Install](#install-1)
- [MacOS](#macos)

# Windows

I have made some wheel distributions that you can ty downloading directly. 

To install use:

```cmd
pip install fastautomata<release version>.whl
```

This should install without any problems, but I have tested very little windows configurations.

To build from source:

## Install dependencies

If you want to build from source, you are going to need the c++ build esencial from visual studio (I hate it, but yeah).

After that, you will need to have the version of python that you have installed ready and available in path. (Python 3.10 or bigger)

Install pybind by running `pip install 'pybind11[Global]'`

Clone the repo to your own computer (using git clone)

## Compile

To compile, I recommend using vscode, but I guess anything works. 

Compilation can be achieved by using the cmake and cmake tools extensions.

I have tested using the `Visual Studio Community 2022 Release - x86_amd64` version, you might have luck using otherwise.

> Note: I tried using the gcc compiler for windows and it did build, but libraries where missing. You can try tho.

If you want fastautomata to run quicker, use the Release configuration.

Finally, once you have all the setup ready, press build. 

A folder named Release or RelWithDebInfo or Debug should have been built. These folders are under the include/fastautomata files (where the cmake file is stored). The files should start with fastautomata_clib.

## Install

Move the binaries under the python files (should be under ./fastautomata/).

To install, run `pip install -e .` withing the parent folder (where the setup.py file is).

> Note: every time you compile, you have to manually move the files

# Linux

To install use:

```cmd
pip install fastautomata<release version>.whl
```

If you are lucky, you can just install the wheel version. It should work but idk. maybe AMD processors need to compile. 

## Install dependencies

install:

- pybind11-dev
- gcc 
- cmake

```sh
sudo apt install -y pybind11-dev gcc cmake
```

## Compile

> Note: you might be able to get away with installing directly by using: `pip install git+https://github.com/MrDrHax/fast-automata.git`

I again used vscode, if you know the commands for cmake go ahead.

Open the root, configure cmake, and press build.

The file will get automatically added to where it should be.

Console should be something like this (idk haven't tried):

```sh
mkdir build
cd build
cmake ../fastautomata/include/fastautomata/CMakeLists.txt
make
```

## Install

To install, run `pip install -e .` withing the parent folder (where the setup.py file is).

# MacOS

I have no fucking idea. If you know how to, feel free to make a pull request.

UwU
