import random
from typing import Optional
from .cell import Cell
from .maze import Maze
from .constants import NORTH, EAST, SOUTH, WEST


class MazeGenerator:
    """
    MazeGenerator implements a randomized depth-first search maze generator
    with optional imperfections (extra openings to create cycles). It also
    computes the shortest path between entry and exit with BFS.

    Example:
        gen = MazeGenerator(20, 15, entry=(0,0), exit=(19,14))
        gen.generate(seed=42, perfect=False)

    Attributes:
        _width (int): maze width in cells.
        _height (int): maze height in cells.
        _entry (tuple[int,int]): (col,row) coordinates of entry.
        _exit (tuple[int,int]): (col,row) coordinates of exit.
        maze (Maze): Maze instance currently generated.
        solution (Optional[list[tuple[int,int]]]): BFS solution path as list
            of (row,col) coordinates or None.
    """

    def __init__(self, width: int, height: int,
                 entry: tuple[int, int] = (0, 0),
                 exit: tuple[int, int] = (0, 0)) -> None:
        """
        Initialize the MazeGenerator.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            entry: (col, row) coordinates for the entry cell.
            exit: (col, row) coordinates for the exit cell.

        Returns:
            None
        """
        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit
        self.maze = Maze(width, height, entry, exit)
        self.solution: Optional[list[tuple[int, int]]] = None

    def generate(self, seed: Optional[int] = None,
                 perfect: bool = True) -> None:
        """
        Generate a new maze using randomized DFS and
        optionally make it imperfect.

        The method:
            - reinitializes the Maze object and matrix,
            - marks the "ft" pattern (forbidden cells),
            - runs iterative DFS from the entry cell,
            - optionally creates extra openings to produce cycles,
            - opens the entry and exit cells,
            - computes and stores the BFS shortest path as self.solution.

        Args:
            seed: Optional random seed to make generation deterministic.
            perfect: If False, extra walls are broken to create cycles.

        Raises:
            ValueError: If entry or exit overlap with forbidden 'ft' cells.

        Returns:
            None
        """
        random.seed(seed)
        self.maze = Maze(self._width, self._height, self._entry, self._exit)
        self.maze.fill_matrix()
        self.maze.fill_ft()

        entry_col, entry_row = self.maze.entry
        exit_col, exit_row = self.maze.exit

        if self.maze.matrix[entry_row][entry_col].ft:
            raise ValueError("ENTRY coordinates overlap with the 42 pattern")
        if self.maze.matrix[exit_row][exit_col].ft:
            raise ValueError("EXIT coordinates overlap with the 42 pattern")

        start = self.maze.matrix[entry_row][entry_col]
        start.mark_visited()
        stack = [start]
        while stack:
            actual = stack[-1]
            neighbors = actual.get_neighbors(
                self.maze.matrix, self.maze.width, self.maze.height
            )

            if neighbors:
                neighbor = random.choice(neighbors)
                self.break_walls_between(actual, neighbor)
                neighbor.mark_visited()
                stack.append(neighbor)
            else:
                stack.pop()

        if not perfect:
            self.make_imperfect()
        self.open_entry_exit()
        self.solution = self._solve_bfs()

    def break_walls_between(self, cell_a: Cell, cell_b: Cell) -> None:
        """
        Break the walls between two adjacent cells symmetrically.

        Determines relative position of cell_b with respect to cell_a and
        calls break_wall on both cells with opposite directions.

        Args:
            cell_a: The current cell (source).
            cell_b: The neighboring cell (target).

        Returns:
            None
        """
        if cell_b.coord[0] < cell_a.coord[0]:
            cell_a.break_wall(NORTH)
            cell_b.break_wall(SOUTH)
        elif cell_b.coord[0] > cell_a.coord[0]:
            cell_a.break_wall(SOUTH)
            cell_b.break_wall(NORTH)
        elif cell_b.coord[1] < cell_a.coord[1]:
            cell_a.break_wall(WEST)
            cell_b.break_wall(EAST)
        elif cell_b.coord[1] > cell_a.coord[1]:
            cell_a.break_wall(EAST)
            cell_b.break_wall(WEST)

    def _would_create_open_area(self, row: int, col: int,
                                direction: int) -> bool:
        """
        Check whether breaking the wall between (row, col) and its neighbor
        in `direction` would produce a fully open 3x3 area.

        After the hypothetical wall removal, every 3x3 block that contains
        the affected edge is tested. A block is considered "open" when all
        internal horizontal and vertical passages are free of walls.

        Args:
            row: Row of the source cell.
            col: Column of the source cell.
            direction: EAST or SOUTH — the wall about to be broken.

        Returns:
            True if at least one 3x3 block would become fully open.
        """
        matrix = self.maze.matrix

        def passage_open(r: int, c: int, d: int) -> bool:
            """Return True if the wall in direction d is already absent,
            OR it is the exact wall we are about to break."""
            if d == EAST:
                if (r == row and c == col and direction == EAST):
                    return True
                if (r == row and c == col + 1 and direction == WEST):
                    return True
            if d == SOUTH:
                if (r == row and c == col and direction == SOUTH):
                    return True
                if (r == row + 1 and c == col and direction == NORTH):
                    return True
            return not matrix[r][c].has_wall(d)

        if direction == EAST:
            candidate_rows = [row - 2, row - 1, row]
            candidate_cols = [col - 1, col]
        else:
            candidate_rows = [row - 1, row]
            candidate_cols = [col - 2, col - 1, col]

        for r0 in candidate_rows:
            for c0 in candidate_cols:
                if r0 < 0 or c0 < 0:
                    continue
                if r0 + 2 >= self.maze.height or c0 + 2 >= self.maze.width:
                    continue
                open_block = True
                for r in range(r0, r0 + 3):
                    if not passage_open(r, c0, EAST):
                        open_block = False
                        break
                    if not passage_open(r, c0 + 1, EAST):
                        open_block = False
                        break
                if open_block:
                    for c in range(c0, c0 + 3):
                        if not passage_open(r0, c, SOUTH):
                            open_block = False
                            break
                        if not passage_open(r0 + 1, c, SOUTH):
                            open_block = False
                            break
                if open_block:
                    return True
        return False

    def make_imperfect(self) -> None:
        """
        Create additional openings in the maze to introduce cycles.

        Iterates all cells and with a small probability breaks east/south walls
        between adjacent non-'ft' cells (avoiding the forbidden pattern).
        A wall is only broken if doing so would NOT create a fully open 3x3
        area (corridors wider than 2 cells are forbidden).

        Returns:
            None
        """
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                cell = self.maze.matrix[row][col]
                if cell.ft:
                    continue
                if col + 1 < self.maze.width:
                    neighbor = self.maze.matrix[row][col + 1]
                    if cell.has_wall(EAST) and not neighbor.ft:
                        if random.random() < 0.2:
                            if not self._would_create_open_area(
                                    row, col, EAST):
                                self.break_walls_between(cell, neighbor)
                if row + 1 < self.maze.height:
                    neighbor = self.maze.matrix[row + 1][col]
                    if cell.has_wall(SOUTH) and not neighbor.ft:
                        if random.random() < 0.2:
                            if not self._would_create_open_area(
                                    row, col, SOUTH):
                                self.break_walls_between(cell, neighbor)

    def open_entry_exit(self) -> None:
        """
        Mark the entry and exit cells on the maze.

        Sets the entry and exit flags on the corresponding cells so the
        renderer and pathfinder can recognize them.

        Returns:
            None
        """
        entry_col, entry_row = self.maze.entry
        entry_cell = self.maze.matrix[entry_row][entry_col]
        entry_cell.mark_entry()

        exit_col, exit_row = self.maze.exit
        exit_cell = self.maze.matrix[exit_row][exit_col]
        exit_cell.mark_exit()

    def _solve_bfs(self) -> Optional[list[tuple[int, int]]]:
        """
        Find the shortest path between entry and exit using BFS.

        The BFS respects walls: movement to a neighbor is allowed only if the
        current cell does not have a wall in that direction.

        Returns:
            A list of (row, col) coordinates from entry to exit (inclusive),
            or None if no path exists.
        """
        entry_col, entry_row = self.maze.entry
        exit_col, exit_row = self.maze.exit

        start = (entry_row, entry_col)
        end = (exit_row, exit_col)

        visited: set[tuple[int, int]] = {start}

        came_from: dict[tuple[int, int], Optional[tuple[int, int]]] = {
            start: None
        }

        queue: list[tuple[int, int]] = [start]

        neighbors_info = [
            (NORTH, -1,  0),
            (SOUTH,  1,  0),
            (EAST,   0,  1),
            (WEST,   0, -1),
        ]

        while queue:
            row, col = queue.pop(0)

            if (row, col) == end:
                return self._reconstruct_path(came_from, end)

            cell = self.maze.matrix[row][col]

            for direction, dr, dc in neighbors_info:
                nrow, ncol = row + dr, col + dc

                if (nrow, ncol) in visited:
                    continue

                if not (0 <= nrow < self.maze.height
                        and 0 <= ncol < self.maze.width):
                    continue

                if cell.has_wall(direction):
                    continue

                visited.add((nrow, ncol))
                came_from[(nrow, ncol)] = (row, col)
                queue.append((nrow, ncol))

        return None

    def _reconstruct_path(
        self,
        came_from: dict[tuple[int, int], Optional[tuple[int, int]]],
        end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        Reconstruct the path from the BFS came_from map.

        Walks backwards from the end coordinate to the start using came_from,
        marks the solution flag on each cell visited, reverses the path and
        returns it.

        Args:
            came_from: Mapping of node -> predecessor from BFS.
            end: End coordinate (row, col) to start reconstruction from.

        Returns:
            The path as a list of (row, col) coordinates in forward order.
        """
        path: list[tuple[int, int]] = []
        current: Optional[tuple[int, int]] = end
        i = 0

        while current is not None:
            path.append(current)
            row, col = current
            self.maze.matrix[row][col].solution = True
            current = came_from[current]
            i += 1

        path.reverse()
        return path

    def verify_coherence(self) -> bool:
        """
        Verify that wall flags between neighboring cells are symmetric.

        Ensures that for every pair of adjacent cells the corresponding walls
        match (east/west and south/north). Prints a message and returns False
        on the first incoherence found.

        Returns:
            True if all neighbor wall flags are coherent, False otherwise.
        """
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                cell = self.maze.matrix[row][col]
                if col + 1 < self.maze.width:
                    neighbor = self.maze.matrix[row][col + 1]
                    if cell.has_wall(EAST) != neighbor.has_wall(WEST):
                        print(f"Incoherence at ({row},{col}) EAST/WEST")
                        return False
                if row + 1 < self.maze.height:
                    neighbor = self.maze.matrix[row + 1][col]
                    if cell.has_wall(SOUTH) != neighbor.has_wall(NORTH):
                        print(f"Incoherence at ({row},{col}) SOUTH/NORTH")
                        return False
        return True
