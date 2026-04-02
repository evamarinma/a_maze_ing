import sys
from .config_parser import Config
from . import MazeGenerator
from .maze_mlx import run_viewer

try:
    if sys.argv[1] != "config.txt":
        raise
    config_txt = sys.argv[1]
except Exception:
    print("Error: Please, provide a valid config file 'config.txt' as the "
          "first argument at execution")
    sys.exit(1)
config = Config(config_txt)
try:
    assert config.entry is not None and config.exit is not None
except AssertionError:
    print("Error: Missing required key/s: ENTRY/EXIT")
    sys.exit(1)
if config.width is not None:
    width = config.width
if config.height is not None:
    height = config.height
generator = MazeGenerator(width, height, config.entry,
                          config.exit)

if config.perfect is not None:
    perfect = config.perfect
try:
    generator.generate(config.seed, perfect)
except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)

directions_map: dict[tuple[int, int], str] = {
    (-1, 0): 'N',
    (1, 0): 'S',
    (0, 1): 'E',
    (0, -1): 'W'
}


def write_maze(generator: MazeGenerator, config: Config) -> None:
    """Write the maze representation and solution to the output file.

    The file format:
        - One line per maze row containing hexadecimal wall flags.
        - A blank line.
        - ENTRY coordinates as "x,y"
        - EXIT coordinates as "x,y"
        - Optional solution path as a sequence of directions (N,S,E,W)

    Args:
        generator: MazeGenerator instance that produced the maze.
        config: Parsed Config with output path and ENTRY/EXIT coordinates.

    Returns:
        None
    """
    if config.output_file is not None:
        output_file = config.output_file
    with open(output_file, "w") as f:
        for row in generator.maze.matrix:
            f.write("".join(hex(cell.walls)[2:].upper() for cell in row) +
                    "\n")
        f.write("\n")
        try:
            assert config.entry is not None and config.exit is not None
        except AssertionError:
            print("Error: Missing required key/s: ENTRY/EXIT")
            sys.exit(1)
        f.write(f"{config.entry[0]},{config.entry[1]}\n")
        f.write(f"{config.exit[0]},{config.exit[1]}\n")
        if generator.solution:
            path_str = ""
            for i in range(1, len(generator.solution)):
                prev = generator.solution[i - 1]
                curr = generator.solution[i]
                dr = curr[0] - prev[0]
                dc = curr[1] - prev[1]
                path_str += directions_map[(dr, dc)]
            f.write(path_str + "\n")


write_maze(generator, config)
print("Maze written to", config.output_file)


def on_regenerate() -> None:
    """Callback to rewrite the maze when the viewer requests regeneration."""
    write_maze(generator, config)


run_viewer(generator.maze, generator, perfect, on_regenerate)
