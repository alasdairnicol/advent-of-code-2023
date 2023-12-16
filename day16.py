#!/usr/bin/env python
from collections import deque
import itertools

Direction = tuple[int, int]
Point = tuple[int, int]
Grid = dict[Point, str]


def parse_grid(lines: list[str]) -> Grid:
    grid = {}
    for j, line in enumerate(lines):
        for i, x in enumerate(line.strip()):
            grid[i, j] = x
    return grid


def next_directions(grid: Grid, point: Point, direction: Direction):
    x, y = point
    dx, dy = direction
    val = grid[point]
    if val == ".":
        yield direction
    elif val == "-":
        if dy == 0:
            yield direction
        else:
            yield (-1, 0)
            yield (1, 0)
    elif val == "\\":
        yield (dy, dx)
    elif val == "|":
        if dx == 0:
            yield direction
        else:
            yield (0, -1)
            yield (0, 1)
        pass
    elif val == "/":
        yield (-dy, -dx)


def num_energized_points(grid: Grid, x: int, y: int, dx: int, dy: int) -> int:
    seen = set()
    queue = deque([(x, y, dx, dy)])
    while queue:
        x, y, dx, dy = queue.popleft()
        if (x, y, dx, dy) in seen:
            continue
        elif (x, y) in grid:
            seen.add((x, y, dx, dy))
            for dx, dy in next_directions(grid, (x, y), (dx, dy)):
                queue.append((x + dx, y + dy, dx, dy))
    return len({(x, y) for (x, y, *_) in seen})


def do_part_1(grid: Grid) -> int:
    return num_energized_points(grid, x=0, y=0, dx=1, dy=0)


def do_part_2(grid: Grid) -> int:
    max_x = max(x for (x, y) in grid)
    max_y = max(y for (x, y) in grid)
    return max(
        itertools.chain(
            (num_energized_points(grid, i, 0, 0, 1) for i in range(max_x + 1)),
            (num_energized_points(grid, i, max_y, 0, -1) for i in range(max_x + 1)),
            (num_energized_points(grid, 0, j, 1, 0) for j in range(max_y + 1)),
            (num_energized_points(grid, max_x, j, -1, 0) for j in range(max_y + 1)),
        )
    )

    return 2


def main():
    lines = [line.strip() for line in read_input()]
    grid = parse_grid(lines)

    part_1 = do_part_1(grid)
    print(f"{part_1=}")

    part_2 = do_part_2(grid)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day16.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
