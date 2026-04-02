
install:
	pip install mlx-1.0.0-py3-none-any.whl
	pip install mypy

run:
	python3 a_maze_ing.py config.txt

debug:
	python -m pdb a_maze_ing.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 . --exclude=mlx,minilibx,venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --strict
	mypy . --strict
