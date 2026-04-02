*This project has been created as part of the 42 curriculum by emarin-m and mabada-r*

# A_MAZE_ING

## :jigsaw: A maze generator program for 42 Cursus

### :open_book: Description
For this project, we're given the task to deliver a program that's able to generate a perfect maze - that meaning the non-existance of cicles in it. Program must be executed by a 'Makefile' that contains several rules, as we'll show later on in this documentation, and translate the walls of the maze on hexadecimal characters, depending on the last 4 bits of each character in 'maze.txt'. 1 means there's a closed wall. 0 means it's open. We'll explain further on this later on as well.

We chose to show the visualization of our maze through MLX. Entry and exit coordenates, as well as the shortest path to solve the maze, are written down on this document too. User should be able to re-generate the maze, show/hide the shortest solution to the maze and change wall colours during execution.

### :open_file_folder: Makefile
Here are some commands available to use the program.
```bash
# Install program dependencies (mlx and mypy)
make install

# Execute program
make run

# Run main script in debug mode
make debug

# Erase temporary files (e.g __pycache__ or .mypy_cache)
make clean

# Check code format and typehint errors using flake8 and mypy
make lint

```
<br>

### :paperclip: User instructions

1. Clone this repository on your computer:
```bash
git clone git@vogsphere-v2.42madrid.com:vogsphere/intra-uuid-7f0a7342-6639-416d-80ed-3eb0d475c353-7269739-mabada-r
```
<button onclick="navigator.clipboard.writeText('clone git@vogsphere-v2.42madrid.com:vogsphere/intra-uuid-7f0a7342-6639-416d-80ed-3eb0d475c353-7269739-mabada-r')"></button>
<br>

2. Create a virtual environment to safely install dependencies. To do so, execute the following command.
```bash
python3 -m venv [venv_name]
```
<button onclick="navigator.clipboard.writeText('python3 -m venv [venv_name]')"></button>
<br>

3. Now, activate the virtual environment so dependencies install inside of it.
```bash
source [venv_name]/bin/activate
```
<button onclick="navigator.clipboard.writeText('source [venv_name]/bin/activate')"></button>
<br>

4. Run **'make install'** command to install mlx and mypy dependencies.
<br>

5. You could run the program now, but let's set 'config.txt' file first. A template has been provided for you in the repository with the exact format the program will be expecting. **'SEED'** field is **optional**. Feel free to play with the initial configuration for the maze.
<br>

    <img width="173" height="134" alt="A screenshot from config.txt file" src="https://i.imgur.com/bOSq6ty.png" />
<br>

6. Execute **'make run'** command. A mlx window will pop up rendering a maze based on the configuration you've previously provided. This is an example of what you should expect.
<br>
    <img width="455" height="465" alt="A screenshot the unsolved maze" src="https://i.imgur.com/BOEMgo1.png" />
<br>
> &nbsp;
> [!warning]
> *Don't try to rescale the window, as it'll produce a segmentation fault.*
> &nbsp;

### :keyboard: User controls

* Press **'ESC'** key to ***exit*** the program.
* Press **'R'** key to ***regenerate*** the maze with same configuration.
* Press **'P'** key to toggle between showing/hidding the ***solution*** path. The solution path should look something like this.
<br>
    <img width="454" height="465" alt="A screenshot from the solved maze" src="https://i.imgur.com/XCavjkZ.png" />
<br>

* Press **'C'** key to change the ***color*** palette for the maze.
<br>
    <img width="454" height="465" alt="A screenshot from the solved maze, different colors" src="https://i.imgur.com/rBhrwu4.png" />
<br>

### :abacus: The algorithm
We use two simple, well-known algorithms combined:

- Maze generation — Randomized Depth‑First Search (iterative backtracker)
  - Start at ENTRY, mark cells visited and push onto a stack.
  - Repeatedly consider the cell on top of the stack, gather its unvisited
    neighbours (ignoring 'ft' forbidden cells), choose one at random,
    break the two corresponding walls symmetrically and push the neighbour.
  - If a cell has no unvisited neighbours, pop (backtrack).
  - This produces a perfect maze (no cycles) and is fast and memory‑efficient.
  - If imperfect mazes are requested, after generation we scan the grid and
    randomly break a small fraction of east/south walls between adjacent
    non‑ft cells to create cycles and multiple routes.

- Maze solving — Breadth‑First Search (BFS)
  - BFS runs from ENTRY and respects walls: a move to a neighbour is allowed
    only when the wall between the two cells is open.
  - BFS finds the shortest path (in number of steps) to EXIT, we reconstruct
    the path using a parent map and mark cells in the solution for rendering.

### :desktop_computer: Maze rendering
For the rendering of this project we used the minilibx library, provided by 42 on the project page. It was a challenge to understand how it worked, pixel by pixel, and working with actual coordenates of the computer screen, but it surely was a rewarding experience. A it's a 'mini' version of an X library, it still has its limitations. If you try to rescale the window, for example, a segmentation fault will occur.
Adding text to the rendering window is rough as well. You can't choose, not only the font, but the size of the characters. We found this was a problem when we wanted to add a responsive desing, depending on the maze proportions. If it was too small, the instructions text would end outside of the window limits. The ideal fix to this problem would have been change text's size, but as it was not possible through mlx, we end up redisigning the whole window depending on maze's proportions.
Overall, beside the library limitations, we like to think we did a good job with it.

### :recycle: Code reusability
The maze generation and solving code is implemented as a small, self-contained Python package so it can be reused independently of the MLX renderer and I/O. This separation makes it easy to import the core API from other projects, write unit tests for the algorithmic parts, or call the generator from scripts.

The project is packaged with setuptools (setup.py). To build installable artifacts run:
```bash
python3 -m pip install --upgrade build
python3 -m build
```
Distributions are produced in dist/.

Install the package for development or use:
```bash
python3 -m pip install -e .
# or install a built wheel:
python3 -m pip install dist/mazegen-1.0.0-py3-none-any.whl
```

After installation the core API is available as:
```py
from mazegen import MazeGenerator
```

### :thought_balloon: Project management
Early on the developing of this project, we decided to work with cell and maze instances so we could store and easily access its properties. If we wanted to know each cell's wall, no matter if it was while generating the maze or solving it, it was as easy as accessing the correct method for that. This gave us the proper tools to work with clean code all along the project. Due to our personal availability, emarin-m started working on the base for the maze and cell classes. From that point forward, mabada-r took on generating and solving algorithms, while emarin-m worked on the mlx rendering code.
In general, we managed to maintain a good balance in task distribution.

### :monocle_face: Resources
https://medium.com/geekculture/backtracking-algorithm-95622dcb6ac8
https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
https://brilliant.org/wiki/recursive-backtracking/
https://www.youtube.com/watch?v=HZ5YTanv5QE