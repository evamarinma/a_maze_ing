from mlx import Mlx
from typing import Any, Optional, Callable
from dataclasses import dataclass
from typing import List, Dict
from .maze import Maze
from .cell import Cell
from .algorithm import MazeGenerator
from .constants import COLOR_PALETTE


@dataclass
class MazeConfig:
    width: int
    height: int
    cell_height: int = 15
    cell_width: int = 15
    cell_wall: int = 2
    win_width: int = 0
    win_height: int = 0
    maze_starting_width = 0
    maze_starting_height = 0


def put_pixel_to_image(img_buff: memoryview, x: int, y: int, color: int,
                       size_line: int, bits_per_pixel: int) -> None:
    """ Sets the color of a specific pixel in the image buffer.

    Args:
        img_buff: The image buffer to modify.
        x: The x-coordinate of the pixel.
        y: The y-coordinate of the pixel.
        color: The color value in 0xRRGGBB format.
        size_line: The size of a line in bytes.
        bits_per_pixel: The number of bits per pixel.

    Returns:
        None
    """
    bytes_per_pixel = bits_per_pixel // 8
    offset = (y * size_line) + (x * bytes_per_pixel)

    blue = color & 0xFF
    green = (color >> 8) & 0xFF
    red = (color >> 16) & 0xFF

    img_buff[offset] = blue
    img_buff[offset + 1] = green
    img_buff[offset + 2] = red
    img_buff[offset + 3] = 255


def render(param: Any) -> None:
    """ Renders the current image and text to the window.

    Args:
        param: Dictionary containing MLX and window parameters.

    Returns:
        None
    """

    param['mlx'].mlx_clear_window(param['mlx_ptr'], param['win'])
    param['mlx'].mlx_put_image_to_window(param['mlx_ptr'], param['win'],
                                         param['img'],
                                         param['paint_starting_width'],
                                         param['paint_starting_height'])
    paint_text(param['mlx'], param['mlx_ptr'], param['win'],
               param['maze_config'])


def key_press(keycode: int, param: Any) -> None:
    """ Handles key press events for the maze viewer.

    Args:
        keycode: The key code of the pressed key.
        param: Dictionary containing MLX and maze parameters.

    Returns:
        None
    """
    if keycode == 65307:  # ESC
        param['mlx'].mlx_loop_exit(param['mlx_ptr'])
    elif keycode == 114:  # R
        param['generator'].generate(None, param['perfect'])
        param['is_solution'] = False
        paint_maze(param['mlx'], param['mlx_ptr'], param['win'],
                   param['maze_config'], param,
                   param['generator'].maze.matrix)
        if param['on_regenerate']:
            param['on_regenerate']()
    elif keycode == 112:  # P
        param['is_solution'] = not param['is_solution']
        paint_maze(param['mlx'], param['mlx_ptr'], param['win'],
                   param['maze_config'], param,
                   param['generator'].maze.matrix)
    elif keycode == 99:  # C
        current_index = param['color_palette'].index(
            param['color']
        )
        if current_index == len(param['color_palette']) - 1:
            current_index = 0
        else:
            current_index += 1
        param['color'] = param['color_palette'][current_index]
        paint_maze(param['mlx'], param['mlx_ptr'], param['win'],
                   param['maze_config'], param,
                   param['generator'].maze.matrix)


def close_window(param: Any) -> None:
    """ Closes the MLX window and exits the main loop.

    Args:
        param: Dictionary containing MLX parameters.

    Returns:
        None
    """
    param['mlx'].mlx_loop_exit(param['mlx_ptr'])


def paint_matrix(image_buff: memoryview, matrix: List[List["Cell"]],
                 maze: "MazeConfig", size_line: int,
                 bits_per_pixel: int, data: dict) -> None:
    """ Paints the maze matrix onto the image buffer.

    Args:
        image_buff: The image buffer to draw on.
        matrix: The matrix of maze cells.
        maze: Maze configuration parameters.
        size_line: The size of a line in bytes.
        bits_per_pixel: The number of bits per pixel.
        data: Additional drawing parameters.

    Returns:
        None
    """
    index = 0
    for matrix_row in matrix:
        for cell in matrix_row:
            row = index // maze.width
            col = index % maze.width
            index += 1
            px_coords = (col * maze.cell_width, row * maze.cell_height)
            if cell.walls == 0xF:
                for i in range(maze.cell_width):
                    for j in range(maze.cell_height):
                        put_pixel_to_image(image_buff, px_coords[0] + i,
                                           px_coords[1] + j,
                                           data['color']['ft'],
                                           size_line, bits_per_pixel)
            else:
                if cell.walls & 1:
                    for i in range(maze.cell_width):
                        for j in range(maze.cell_wall):
                            put_pixel_to_image(image_buff, px_coords[0] + i,
                                               px_coords[1] + j,
                                               data['color']['walls'],
                                               size_line, bits_per_pixel)
                if cell.walls & 2:
                    for i in range(maze.cell_height):
                        for j in range(maze.cell_wall):
                            put_pixel_to_image(image_buff, px_coords[0] +
                                               (maze.cell_width -
                                                maze.cell_wall) + j,
                                               px_coords[1] + i,
                                               data['color']['walls'],
                                               size_line, bits_per_pixel)
                if cell.walls & 4:
                    for i in range(maze.cell_width):
                        for j in range(maze.cell_wall):
                            put_pixel_to_image(image_buff, px_coords[0] + i,
                                               (maze.cell_height -
                                               maze.cell_wall) + px_coords[1] +
                                               j,
                                               data['color']['walls'],
                                               size_line, bits_per_pixel)
                if cell.walls & 8:
                    for i in range(maze.cell_height):
                        for j in range(maze.cell_wall):
                            put_pixel_to_image(image_buff, px_coords[0] + j,
                                               px_coords[1] + i,
                                               data['color']['walls'],
                                               size_line, bits_per_pixel)
                # rellenamos la celda si es solución
                if data['is_solution']:
                    if cell.solution:
                        for i in range(maze.cell_width - (maze.cell_wall * 2)):
                            for j in range(maze.cell_height - (maze.cell_wall *
                                                               2)):
                                put_pixel_to_image(image_buff, px_coords[0] +
                                                   (i + maze.cell_wall),
                                                   px_coords[1] +
                                                   (j + maze.cell_wall),
                                                   data['color']['solution'],
                                                   size_line,
                                                   bits_per_pixel)
                if cell.entry:
                    for i in range(maze.cell_width - (maze.cell_wall * 2)):
                        for j in range(maze.cell_height - (maze.cell_wall *
                                                           2)):
                            put_pixel_to_image(image_buff, px_coords[0] +
                                               (i + maze.cell_wall),
                                               px_coords[1] +
                                               (j + maze.cell_wall),
                                               data['color']['entry'],
                                               size_line,
                                               bits_per_pixel)
                if cell.exit:
                    for i in range(maze.cell_width - (maze.cell_wall * 2)):
                        for j in range(maze.cell_height -
                                       (maze.cell_wall * 2)):
                            put_pixel_to_image(image_buff, px_coords[0] +
                                               (i + maze.cell_wall),
                                               px_coords[1] +
                                               (j + maze.cell_wall),
                                               data['color']['exit'],
                                               size_line,
                                               bits_per_pixel)


def paint_maze(a: "Mlx", mlx_ptr: int, win: Any,
               maze_config: "MazeConfig", data: dict,
               matrix: List[List["Cell"]]) -> None:
    """ Draws the maze on the window using the provided matrix.

    Args:
        a: The MLX instance.
        mlx_ptr: The MLX pointer.
        win: The window object.
        maze_config: Maze configuration parameters.
        data: Additional drawing parameters.
        matrix: The matrix of maze cells.

    Returns:
        None
    """
    maze_img = a.mlx_new_image(mlx_ptr, (maze_config.width *
                               maze_config.cell_width),
                               maze_config.height * maze_config.cell_height)
    img_buff, bits_per_pixel, size_line, endian = a.mlx_get_data_addr(maze_img)
    img_buff[:] = bytes(len(img_buff))

    # Render image in window
    data['img'] = maze_img
    maze_config.maze_starting_width = ((maze_config.win_width -
                                        (maze_config.width *
                                            maze_config.cell_width)) // 2)
    data['paint_starting_width'] = maze_config.maze_starting_width
    if maze_config.width > 17:
        maze_config.maze_starting_height = (((maze_config.win_height -
                                            (maze_config.height *
                                             maze_config.cell_height)) // 2) -
                                            maze_config.cell_height * 2)
    else:
        maze_config.maze_starting_height = (((maze_config.win_height -
                                            (maze_config.height *
                                             maze_config.cell_height)) // 2) -
                                            maze_config.cell_height * 4)
    data['paint_starting_height'] = maze_config.maze_starting_height
    paint_matrix(img_buff, matrix, maze_config,
                 size_line, bits_per_pixel, data)
    a.mlx_put_image_to_window(mlx_ptr, win, maze_img,
                              maze_config.maze_starting_width,
                              maze_config.maze_starting_height)


def set_mlx_win(a: "Mlx", mlx_ptr: int, maze_config: "MazeConfig") -> object:
    """ Sets up the MLX window with the appropriate size for the maze.

    Args:
        a: The MLX instance.
        mlx_ptr: The MLX pointer.
        maze_config: Maze configuration parameters.

    Returns:
        object: The created window object.
    """
    if maze_config.height < 20:
        height_multiplier = maze_config.cell_height * 2
    elif maze_config.height >= 20 and maze_config.height < 30:
        height_multiplier = round(maze_config.cell_height * 1.3)
    elif maze_config.height >= 30 and maze_config.height < 50:
        height_multiplier = round(maze_config.cell_height * 1.4)
    elif maze_config.height >= 50 and maze_config.height < 80:
        height_multiplier = round(maze_config.cell_height * 1.3)
    else:
        height_multiplier = round(maze_config.cell_height * 1.2)
    if maze_config.width > 17:
        if maze_config.width < 40:
            maze_config.win_width = round(maze_config.width *
                                          (maze_config.cell_width * 1.5))
            maze_config.win_height = round(maze_config.height *
                                           height_multiplier)
        elif maze_config.width >= 40 and maze_config.width < 60:
            maze_config.win_width = round(maze_config.width *
                                          (maze_config.cell_width * 1.2))
            maze_config.win_height = round(maze_config.height *
                                           (height_multiplier))
        elif maze_config.width >= 60 and maze_config.width <= 90:
            maze_config.cell_width = 10
            maze_config.cell_height = 10
            maze_config.win_width = round(maze_config.width *
                                          (maze_config.cell_width * 1.1))
            maze_config.win_height = round(maze_config.height *
                                           (height_multiplier))
        else:
            maze_config.cell_width = 8
            maze_config.cell_height = 8
            maze_config.cell_wall = 1
            maze_config.win_width = round(maze_config.width *
                                          (maze_config.cell_width * 1.1))
            maze_config.win_height = round(maze_config.height *
                                           (height_multiplier))
    else:
        if maze_config.width > 10:
            maze_config.win_width = round(maze_config.width *
                                          (maze_config.cell_width * 1.5))
            maze_config.win_height = round(maze_config.height *
                                           (height_multiplier))
        else:
            maze_config.win_width = 200
            maze_config.win_height = round(maze_config.height *
                                           (height_multiplier))
    win = a.mlx_new_window(mlx_ptr, maze_config.win_width,
                           maze_config.win_height, "a-maze-ing")
    return win


def paint_text(a: "Mlx", mlx_ptr: int, win: Any,
               maze_config: "MazeConfig") -> None:
    """ Draws instructions text at the bottom margin of the window.

    Args:
        a: The MLX instance.
        mlx_ptr: The MLX pointer.
        win: The window object.
        maze_config: Maze configuration parameters.

    Returns:
        None
    """
    text_y = ((maze_config.maze_starting_height +
              (maze_config.height * maze_config.cell_height)) +
              maze_config.cell_height)
    if maze_config.width > 17 and maze_config.width <= 90:
        a.mlx_string_put(mlx_ptr, win, maze_config.maze_starting_width,
                         text_y, 0xFFFFFF, "R: Regenerate  ESC: Exit")
        a.mlx_string_put(mlx_ptr, win, maze_config.maze_starting_width,
                         (round(text_y + maze_config.cell_height * 1.6)),
                         0xFFFFFF,
                         "P: Pathfinder  C: Toggle color")
    elif maze_config.width > 90:
        a.mlx_string_put(mlx_ptr, win, maze_config.maze_starting_width,
                         text_y, 0xFFFFFF, "R: Regenerate  ESC: Exit")
        a.mlx_string_put(mlx_ptr, win, maze_config.maze_starting_width,
                         (round(text_y + maze_config.cell_height * 2.5)),
                         0xFFFFFF,
                         "P: Pathfinder  C: Toggle color")
    else:
        if maze_config.width < 10:
            text_width_start = 20
        else:
            text_width_start = maze_config.maze_starting_width
        a.mlx_string_put(mlx_ptr, win, text_width_start,
                         text_y, 0xFFFFFF, "R: Regenerate")
        a.mlx_string_put(mlx_ptr, win, text_width_start,
                         (round(text_y + maze_config.cell_height * 1.6)),
                         0xFFFFFF, "ESC: Exit")
        a.mlx_string_put(mlx_ptr, win, text_width_start,
                         (round(text_y + maze_config.cell_height * (1.6 *
                          2))), 0xFFFFFF, "P: Pathfinder")
        a.mlx_string_put(mlx_ptr, win, text_width_start,
                         (round(text_y + maze_config.cell_height * (1.6 *
                          3))), 0xFFFFFF, "C: Toggle color")


def set_data(maze_config: "MazeConfig", generator: "MazeGenerator",
             perfect: bool,
             on_regenerate: Optional[Callable] = None) -> Dict[str, Any]:
    """ Initializes the data dictionary for the maze viewer.

    Args:
        maze_config: Maze configuration parameters.
        generator: The maze generator instance.
        perfect: Whether the maze is perfect.
        on_regenerate: Callback for regeneration.

    Returns:
        The initialized data dictionary.
    """
    data: Dict[str, Any] = {}
    data['maze_config'] = maze_config
    data['generator'] = generator
    data['perfect'] = perfect
    data['is_solution'] = False
    data['color_palette'] = COLOR_PALETTE
    data['color'] = COLOR_PALETTE[0]
    data['on_regenerate'] = on_regenerate
    return data


def run_viewer(maze: "Maze", generator: "MazeGenerator", perfect: bool,
               on_regenerate: Optional[Callable]) -> None:
    """ Runs the maze viewer, initializing MLX and handling events.

    Args:
        maze: The maze instance to display.
        generator: The maze generator instance.
        perfect: Whether the maze is perfect.
        on_regenerate: Callback for regeneration.

    Returns:
        None
    """
    maze_config = MazeConfig(
        width=maze.width,
        height=maze.height
    )
    data = set_data(maze_config, generator, perfect, on_regenerate)
    a = Mlx()
    data['mlx'] = a
    if a is None:
        raise RuntimeError("Failed to create mlx instance")
    mlx_ptr = a.mlx_init()
    data['mlx_ptr'] = mlx_ptr
    if mlx_ptr is None:
        raise RuntimeError("mlx_init failed")
    win = set_mlx_win(a, mlx_ptr, maze_config)
    data['win'] = win
    paint_maze(a, mlx_ptr, win, maze_config, data, maze.matrix)

    # Hooks
    a.mlx_key_hook(win, key_press, data)
    a.mlx_hook(win, 33, 1 << 17, close_window, data)
    a.mlx_loop_hook(mlx_ptr, render, data)
    # Loop
    a.mlx_loop(mlx_ptr)
