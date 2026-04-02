from .constants import NORTH, EAST, SOUTH, WEST


class Cell:
    """ Represents a single cell in the maze grid.

        Args:
            coord: Position of the Cell as (x, y).

        Attributes:
            coord: Position of the Cell as (x, y).
            walls: Bitmask representing active walls(N, W, S, W).
            visited: Whether the Cell has been visited.
            entry: Whether this Cell is the maze entrance.
            exit: Whether this Cell is the maze exit.
            ft: Whether this Cell is part of the 42 pattern.
            solution: Whether this cell is part of the solution path.
    """

    def __init__(self, coord: tuple[int, int]):
        """ Initializes Cell instance """
        self.coord = coord
        self.walls = NORTH | EAST | SOUTH | WEST
        self.visited = False
        self.entry = False
        self.exit = False
        self.ft = False
        self.solution = False

    def break_wall(self, direction: int) -> None:
        """ Breaks a wall in the given direction (NORTH,
        EAST, SOUTH, WEST)

        Args:
            direction: Represents the given direction.
        Returns:
            None
        """
        self.walls = self.walls & ~direction
        """ Ejemplo:
            celda por defecto = 1111 (todas las paredes cerradas)
            queremos romper NORTH = 0001
            primero ~NORTH -> invierte bits a 1110
            luego
            cell (1111)
               &
            NORTH (1110)
            = 1110 -> Se ha roto sólo la pared NORTH
            """

    def has_wall(self, direction: int) -> int:
        """ Checks if there's a wall in the given direction

        Args:
            direction: Represents the given direction.
        Returns:
            1 if there's a wall in the given direction, 0 if there's not.
        """
        if self.walls & direction:
            return 1
        return 0

    def mark_visited(self) -> None:
        """ Marks itself as visited Cell """
        self.visited = True

    def mark_entry(self) -> None:
        """ Marks itself as 'entry' Cell """
        self.entry = True

    def mark_exit(self) -> None:
        """ Marks itself as 'exit' Cell """
        self.exit = True

    def mark_ft(self) -> None:
        """ Marks itself as 'ft' Cell """
        self.ft = True

    def is_border(self, width: int, height: int) -> int:
        """ Checks if the given Cell is at one of maze's borders

        Args:
            width: Represents maze's width.
            height: Represents maze's height.
        Returns:
            1 if Cell's at maze's border, else returns 0.
        """
        row, col = self.coord
        if row == 0 or col == 0 or row == height - 1 or col == width - 1:
            return 1
        return 0

    @staticmethod
    def find_cell(cell_map: list[list["Cell"]], x: int, y: int) -> "Cell":
        """ Looks for the Cell instance that matches the coordenates received

        Args:
            cell_map: Maze's matrix instance. A list of Cell instances.
            x: Horizontal coordinate of the target Cell.
            y: Vertical coordinate of the target Cell.
        Returns:
            The Cell instance matching the given coordinates.
        """
        return cell_map[x][y]

    def get_neighbors(self, cell_map: list[list["Cell"]], width: int,
                      height: int) -> list:
        """ Returns a list with the valid neighbors of the given Cell instance

        Args:
            cell_map: 2D list of Cell objects to search in.
            width: Maze's width.
            height: Maze's height.
        Returns:
            A list of valid Cell instances neighbors from the given Cell.
        """
        neighbors = []
        if self.coord[0] - 1 >= 0:
            other = Cell.find_cell(cell_map, self.coord[0] - 1, self.coord[1])
            if not other.ft and not other.visited:
                neighbors.append(other)
        if self.coord[0] + 1 < height:
            other = Cell.find_cell(cell_map, self.coord[0] + 1, self.coord[1])
            if not other.ft and not other.visited:
                neighbors.append(other)
        if self.coord[1] - 1 >= 0:
            other = Cell.find_cell(cell_map, self.coord[0], self.coord[1] - 1)
            if not other.ft and not other.visited:
                neighbors.append(other)
        if self.coord[1] + 1 < width:
            other = Cell.find_cell(cell_map, self.coord[0], self.coord[1] + 1)
            if not other.ft and not other.visited:
                neighbors.append(other)
        return neighbors
