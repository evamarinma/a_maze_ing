from .cell import Cell


class Maze:
    """Represents the maze.

    Args:
        width: Maze's width.
        height: Maze's height.
        entry: Coordinates for the entry cell.
        exit: Coordinates for the exit cell.

    Attributes:
        width: Maze's width.
        height: Maze's height.
        entry: Coordinates for the entry cell.
        exit: Coordinates for the exit cell.
        matrix: 2D list of Cell objects representing maze's grid.
        ft_odd: 42 pattern for odd width.
        ft_even: 42 pattern for even width.
    """
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.matrix: list[list["Cell"]] = []
        self.ft_odd = [
            ['█', ' ', ' ', ' ', '█', '█', '█'],
            ['█', ' ', ' ', ' ', ' ', ' ', '█'],
            ['█', '█', '█', ' ', '█', '█', '█'],
            [' ', ' ', '█', ' ', '█', ' ', ' '],
            [' ', ' ', '█', ' ', '█', '█', '█']
        ]
        self.ft_even = [
            ['█', ' ', ' ', ' ', ' ', '█', '█', '█'],
            ['█', ' ', ' ', ' ', ' ', ' ', ' ', '█'],
            ['█', '█', '█', ' ', ' ', '█', '█', '█'],
            [' ', ' ', '█', ' ', ' ', '█', ' ', ' '],
            [' ', ' ', '█', ' ', ' ', '█', '█', '█']
        ]

    def fill_matrix(self) -> None:
        """Fill maze's matrix with Cell instances."""
        i = 0
        while i < self.height:
            j = 0
            row = []
            while j < self.width:
                row.append(Cell((i, j)))
                j += 1
            self.matrix.append(row)
            i += 1

    def fill_ft(self) -> None:
        """Fill maze's 42 pattern depending on maze's width."""
        if self.width % 2 == 0:
            pattern = self.ft_even
        else:
            pattern = self.ft_odd

        pattern_width = len(pattern[0])
        pattern_height = len(pattern)

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print("Maze too small to display 42 pattern")
            return

        if self.width % 2 == 0:
            starting_col = (self.width // 2) - 4
        else:
            starting_col = ((self.width + 1) // 2) - 4
        starting_row = (self.height // 2) - 2

        i = 0
        while i < pattern_height:
            j = 0
            temp_col = starting_col
            while j < pattern_width:
                if pattern[i][j] == '█':
                    self.matrix[starting_row][temp_col].ft = True
                j += 1
                temp_col += 1
            i += 1
            starting_row += 1

    @staticmethod
    def get_len(value: str) -> int:
        """Get the length of a string.

        Args:
            value: The string to measure.

        Returns:
            The length of the string.
        """
        return len(value)

    def __str__(self) -> str:
        """Return string representation of the maze."""
        return str(self.matrix)

    def __len__(self) -> int:
        """Return the number of rows in the maze."""
        return len(self.matrix)
