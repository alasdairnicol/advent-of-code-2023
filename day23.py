#!/usr/bin/env python
from collections import deque
from typing import Generator

Grid = dict[tuple[int, int], str]


def parse_grid(lines: list[str]) -> Grid:
    return {
        (i, j): val
        for j, line in enumerate(lines)
        for i, val in enumerate(line.strip())
        if val != "#"
    }


def next_steps(
    node: tuple[int, int], val: str, downhill_only: bool
) -> Generator[tuple[int, int], None, None]:
    i, j = node
    if downhill_only and val != ".":
        if val == ">":
            yield (i + 1, j)
        elif val == "v":
            yield (i, j + 1)
        elif val == "<":
            yield (i - 1, j)
        elif val == "^":
            # doesn't appear to be in input but include for completeness
            yield (i, j - 1)
    else:
        yield (i + 1, j)
        yield (i, j + 1)
        yield (i - 1, j)
        yield (i, j - 1)


Neighbours = dict[tuple[int, int], dict[tuple[int, int], int]]


def get_neighbours(grid: Grid, downhill_only: bool) -> Neighbours:
    return {
        g: {n: 1 for n in next_steps(g, grid[g], downhill_only) if n in grid}
        for g in grid
    }


def do_part_1(grid: Grid, start: tuple[int, int], end: tuple[int, int]) -> int:
    solutions = []
    queue: deque = deque()
    queue.append((start,))

    while queue:
        path = queue.popleft()
        current_node = path[-1]
        current_val = grid[current_node]
        for node in next_steps(current_node, current_val, downhill_only=True):
            if node == end:
                solutions.append(path + (end,))
            elif node in grid and node not in path:
                queue.append(path + (node,))

    return max(len(solution) - 1 for solution in solutions)


def simplify_neighbours(neighbours: Neighbours):
    while True:
        try:
            node, node_edges = next(
                ((k, v) for k, v in neighbours.items() if len(v) == 2)
            )
        except StopIteration:
            break
        n1, n2 = node_edges

        distance = sum(node_edges.values())
        del neighbours[node]
        del neighbours[n1][node]
        del neighbours[n2][node]
        neighbours[n1][n2] = distance
        neighbours[n2][n1] = distance
    return neighbours


def do_part_2(grid: Grid, start: tuple[int, int], end: tuple[int, int]) -> int:
    neighbours = get_neighbours(grid, downhill_only=False)
    simplify_neighbours(neighbours)
    solutions = []
    queue: deque = deque()
    queue.append(((start,), 0))

    while queue:
        path, cost = queue.popleft()
        current_node = path[-1]
        for new_node, new_cost in neighbours[current_node].items():
            if new_node == end:
                solutions.append((path + (new_node,), cost + new_cost))
            elif new_node not in path:
                queue.append((path + (new_node,), cost + new_cost))

    return max(s[1] for s in solutions)


def main():
    lines = [line.strip() for line in read_input()]

    grid = parse_grid(lines)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)
    start = next(iter((x, y) for (x, y), v in grid.items() if y == min_y))
    end = next(iter((x, y) for (x, y), v in grid.items() if y == max_y))

    part_1 = do_part_1(grid, start, end)
    print(f"{part_1=}")

    part_2 = do_part_2(grid, start, end)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day23.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
