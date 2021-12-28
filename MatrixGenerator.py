from typing import Tuple, List
import numpy as np
import re


def convert_to_int_list(string_rule):
    return [int(x) for x in list(string_rule)]


def parse_rule(rule: str):
    DEFAULT_RULE = "23/3"
    pattern = re.compile("[0-9]{0,5}/[0-9]{0,5}")

    if pattern.match(rule):
        rules = re.split('/', rule)
    else:
        rules = re.split('/', DEFAULT_RULE)
    alive_rule = convert_to_int_list(rules[0])
    dead_rule = convert_to_int_list(rules[1])
    return alive_rule, dead_rule


class MatrixGenerator:
    def __init__(self,
                 matrix_size: Tuple[int, int],
                 number_of_epochs: int,
                 initial_life_probability=0.2) -> None:
        super().__init__()
        self.initial_life_probability = initial_life_probability
        self.number_of_epochs = number_of_epochs
        self.matrix_size = matrix_size

    def generate_GoF_matrices(self, rule: str) -> List[List[List[int]]]:
        (alive_rule, dead_rule) = parse_rule(rule)
        (x_size, y_size) = self.matrix_size
        grid = np.random.choice([0, 1], (x_size, y_size),
                                p=[1 - self.initial_life_probability, self.initial_life_probability])

        matrices =[]
        for _ in range(self.number_of_epochs):
            grid = self.perform_epoch(grid, alive_rule, dead_rule)
            matrices.append(grid)

        return matrices

    def perform_epoch(self, grid, alive_rule, dead_rule):
        (x_size, y_size) = self.matrix_size
        newGrid = grid.copy()

        for row in range(x_size):
            for col in range(y_size):
                alive_neighbors = 0
                dead_neighbors = 0
                actual_cell = grid[row][col]
                for neighbor_row in range(-1, 2):
                    for neighbor_col in range(-1, 2):
                        if not (neighbor_row == 0 and neighbor_col == 0):
                            if grid[(row + neighbor_row) % x_size][(col + neighbor_col) % y_size] == 1:
                                alive_neighbors = alive_neighbors + 1
                            else:
                                dead_neighbors = dead_neighbors + 1
                if actual_cell == 1:
                    if alive_neighbors not in alive_rule:
                        newGrid[row, col] = 0
                if actual_cell == 0:
                    if alive_neighbors in dead_rule:
                        newGrid[row, col] = 1

        grid[:] = newGrid[:]
        return grid
