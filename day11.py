#!/usr/bin/env python
import itertools
from typing import Iterable

Point = tuple[int, int]


def parse_grid(lines: list[str]) -> set:
    grid = set()
    for j, line in enumerate(lines):
        for i, val in enumerate(line):
            if val == "#":
                grid.add((i, j))
    return grid


def get_empty_rows(lines: Iterable[Iterable]) -> set[int]:
    return {j for j, line in enumerate(lines) if "#" not in line}


def get_empty_columns(lines: list[str]) -> set[int]:
    return get_empty_rows(list(zip(*lines)))


def calc_distance(
    point_a: Point,
    point_b: Point,
    empty_columns: set[int],
    empty_rows: set[int],
    expansion_factor: int = 2,
) -> int:
    x_min, x_max = sorted([point_a[0], point_b[0]])
    y_min, y_max = sorted([point_a[1], point_b[1]])
    return (
        (x_max - x_min)
        + (expansion_factor - 1)
        * len([x for x in range(x_min + 1, x_max) if x in empty_columns])
        + (y_max - y_min)
        + (expansion_factor - 1)
        * len([y for y in range(y_min + 1, y_max) if y in empty_rows])
    )


def do_part_1(grid):
    return 10


def main():
    lines = read_input()
    grid = parse_grid(lines)
    empty_rows = get_empty_rows(lines)
    empty_columns = get_empty_columns(lines)

    part_1 = sum(
        calc_distance(point_a, point_b, empty_columns, empty_rows)
        for point_a, point_b in itertools.combinations(grid, 2)
    )

    print(f"{part_1=}")

    part_2 = sum(
        calc_distance(
            point_a, point_b, empty_columns, empty_rows, expansion_factor=1_000_000
        )
        for point_a, point_b in itertools.combinations(grid, 2)
    )

    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day11.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
