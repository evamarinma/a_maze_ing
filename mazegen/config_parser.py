from typing import Tuple, Optional
import sys

Coordinate = Tuple[int, int]


class Config:
    """Parse and validate a simple configuration file.

    This class reads a configuration file containing key=value pairs,
    converts values to appropriate Python types and validates required
    constraints (positive sizes, coordinates within bounds, required keys
    present, etc).

    Example:
        cfg = Config("config.txt")
        print(cfg.width, cfg.height, cfg.entry, cfg.exit)

    Attributes:
        width (int): Maze width in cells.
        height (int): Maze height in cells.
        entry (Optional[Coordinate]): ENTRY coordinate as (x, y).
        exit (Optional[Coordinate]): EXIT coordinate as (x, y).
        output_file (str): Output file path.
        perfect (bool): Whether the maze must be perfect.
        seed (Optional[int]): Optional RNG seed.
    """

    def __init__(self, config_file: str) -> None:
        """Initialize the parser, read and validate the configuration file.

        Opens the given file, parses lines and validates mandatory keys. On
        error it prints a message and exits the program with code 1.

        Args:
            config_file: Path to the configuration file.

        Returns:
            None
        """
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        self.entry: Optional[Coordinate] = None
        self.exit: Optional[Coordinate] = None
        self.output_file: Optional[str] = None
        self.perfect: Optional[bool] = None
        self.seed: Optional[int] = None

        try:
            self._parse_file(config_file)
            self._validate()
            print("Config file read successfully")
        except Exception as e:
            print(f"Config Error: {e}")
            sys.exit(1)

    def _parse_file(self, config_file: str) -> None:
        """Read the configuration file and process each non-empty line.

        Expected format is key=value. Blank lines and lines starting with '#'
        are ignored. Lines without '=' raise a ValueError.
        Each parsed key/value pair is forwarded to _process_line.

        Args:
            config_file: Path to the configuration file.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be read.
            Exception: For other read errors.

        Returns:
            None
        """
        try:
            with open(config_file, "r") as f:
                for lineno, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        raise ValueError(f"Line {lineno}: missing '='")
                    key, value = map(str.strip, line.split("=", 1))
                    self._process_line(key, value)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file '{config_file}' not found")
        except PermissionError:
            raise PermissionError(f"Permission denied to read '{config_file}'")
        except Exception as e:
            raise Exception(f"Error reading configuration file: {e}")

    def _process_line(self, key: str, value: str) -> None:
        """Convert a key/value pair to the correct type and assign to fields.

        Supported keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT, SEED.
        ENTRY and EXIT expect 'x,y' format. Invalid values raise ValueError.

        Args:
            key: Configuration key.
            value: String value associated with the key.

        Raises:
            ValueError: If key is unknown or value cannot be converted.

        Returns:
            None
        """
        try:
            if key == "WIDTH":
                if self.width is not None:
                    raise ValueError("Duplicate key 'WIDTH'")
                self.width = int(value)
            elif key == "HEIGHT":
                if self.height is not None:
                    raise ValueError("Duplicate key 'HEIGHT'")
                self.height = int(value)
            elif key == "ENTRY":
                if self.entry is not None:
                    raise ValueError("Duplicate key 'ENTRY'")
                x, y = map(int, value.split(","))
                self.entry = (x, y)
            elif key == "EXIT":
                if self.exit is not None:
                    raise ValueError("Duplicate key 'EXIT'")
                x, y = map(int, value.split(","))
                self.exit = (x, y)
            elif key == "OUTPUT_FILE":
                if self.output_file is not None:
                    raise ValueError("Duplicate key 'OUTPUT_FILE'")
                self.output_file = value
            elif key == "PERFECT":
                if self.perfect is not None:
                    raise ValueError("Duplicate key 'PERFECT'")
                if value == "True":
                    self.perfect = True
                elif value == "False":
                    self.perfect = False
                else:
                    raise ValueError("PERFECT must be True or False")
            elif key == "SEED":
                if self.seed is not None:
                    raise ValueError("Duplicate key 'SEED'")
                self.seed = int(value)
            else:
                raise ValueError(f"Unknown key '{key}'")
        except Exception as e:
            raise ValueError(f"Error processing '{key}': {e}")

    def _validate(self) -> None:
        """Validate that required fields are present and values are sane.

        Checks that WIDTH and HEIGHT are positive, OUTPUT_FILE, ENTRY and EXIT
        are provided, ENTRY != EXIT and coordinates lie within bounds.

        Raises:
            ValueError: If any validation check fails.

        Returns:
            None
        """
        if self.width is not None and self.width <= 0:
            raise ValueError("WIDTH must be a positive integer")
        if self.width is not None and self.width > 200:
            raise ValueError("WIDTH should not exceed 200")
        if self.height is not None and self.height <= 0:
            raise ValueError("HEIGHT must be a positive integer")
        if self.height is not None and self.height > 200:
            raise ValueError("HEIGHT should not exceed 200")
        if self.output_file == "":
            raise ValueError("Missing required key: OUTPUT_FILE")
        if self.entry is None:
            raise ValueError("Missing required key: ENTRY")
        if self.exit is None:
            raise ValueError("Missing required key: EXIT")
        if self.perfect is None:
            raise ValueError("Missing required key: PERFECT")
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different")
        for name, coord in [("ENTRY", self.entry), ("EXIT", self.exit)]:
            x, y = coord
            if (self.width is not None and not (0 <= x < self.width)
                    or self.height is not None and not (0 <= y < self.height)):
                raise ValueError(
                    f"{name} coordinates {coord} out of bounds"
                )

    def __repr__(self) -> str:
        """Return a string representation of the Config object.

        Returns:
            A string containing the main configuration values.
        """
        return (
            f"Config(width={self.width}, height={self.height}, "
            f"entry={self.entry}, exit={self.exit}, "
            f"output_file='{self.output_file}', "
            f"perfect={self.perfect}, seed={self.seed})"
        )


def parse_config(config_file: str) -> Config:
    """Helper to create and return a validated Config instance.

    Args:
        config_file: Path to the configuration file.

    Returns:
        Config: The created and validated configuration object.
    """
    return Config(config_file)
