#!/usr/bin/env python
def parse_grid(lines: list[str]) -> dict[tuple[int, int], str]:
    grid = {}
    for j, line in enumerate(lines):
        for i, val in enumerate(line):
            if val != ".":
                grid[(i, j)] = val
    return grid


def find_neighbours(grid, start_point):
    for direction, shapes in [
        ((1, 0), {"-", "J", "7"}),
        ((0, 1), {"|", "L", "J"}),
        ((-1, 0), {"-", "F", "L"}),
        ((0, -1), {"|", "7", "F"}),
    ]:
        neighbour = (start_point[0] + direction[0], start_point[1] + direction[1])
        if neighbour in grid and grid[neighbour] in shapes:
            yield neighbour, direction


def next_point(grid, point, direction):
    new_direction_dict = {
        ((1, 0), "-"): (1, 0),
        ((1, 0), "J"): (0, -1),
        ((1, 0), "7"): (0, 1),
        ((0, 1), "|"): (0, 1),
        ((0, 1), "L"): (1, 0),
        ((0, 1), "J"): (-1, 0),
        ((-1, 0), "-"): (-1, 0),
        ((-1, 0), "F"): (0, 1),
        ((-1, 0), "L"): (0, -1),
        ((0, -1), "|"): (0, -1),
        ((0, -1), "7"): (-1, 0),
        ((0, -1), "F"): (1, 0),
    }
    direction = new_direction_dict[(direction, grid[point])]
    point = (point[0] + direction[0], point[1] + direction[1])
    return point, direction


def find_start(grid):
    start = None
    for k, v in grid.items():
        if v == "S":
            start = k
            break
    return start


def do_part_1(grid, start):
    point, direction = next(find_neighbours(grid, start))
    count = 1
    while point != start:
        point, direction = next_point(grid, point, direction)
        count += 1
    return count // 2


def subgrid(point, value):
    x, y = point
    if value == "|":
        return {(2 * x + 1, 2 * y), (2 * x + 1, 2 * y + 1), (2 * x + 1, 2 * y + 2)}
    elif value == "-":
        return {(2 * x + 2, 2 * y + 1), (2 * x + 1, 2 * y + 1), (2 * x + 2, 2 * y + 1)}
    elif value == "J":
        return {(2 * x, 2 * y + 1), (2 * x + 1, 2 * y + 1), (2 * x + 1, 2 * y)}
    elif value == "L":
        return {(2 * x + 1, 2 * y), (2 * x + 1, 2 * y + 1), (2 * x + 2, 2 * y + 1)}
    elif value == "7":
        return {(2 * x, 2 * y + 1), (2 * x + 1, 2 * y + 1), (2 * x + 1, 2 * y + 2)}
    elif value == "F":
        return {(2 * x + 1, 2 * y + 2), (2 * x + 1, 2 * y + 1), (2 * x + 2, 2 * y + 1)}
    elif value == "S":
        return set()
    else:
        raise ValueError(repr(value))


def start_shape(directions):
    if (-1, 0) in directions and (1, 0) in directions:
        return "-"
    elif (0, -1) in directions and (0, 1) in directions:
        return "|"
    elif (-1, 0) in directions and (0, -1) in directions:
        return "J"
    elif (0, -1) in directions and (1, 0) in directions:
        return "L"
    elif (1, 0) in directions and (0, 1) in directions:
        return "F"
    elif (0, 1) in directions and (-1, 0) in directions:
        return "7"


def do_part_2(lines, grid, start):
    directions = [direction for _, direction in find_neighbours(grid, start)]
    start_value = start_shape(directions)
    grid[start] = start_value

    # Get a list of all the points in the loop, because we're going to ignore everything else
    point, direction = next(find_neighbours(grid, start))
    loop = [start]
    while point != start:
        loop.append(point)
        point, direction = next_point(grid, point, direction)

    grid2 = {}

    for point in loop:
        for s in subgrid(point, grid[point]):
            grid2[s] = "█"

    height = len(lines)
    width = len(lines[0])

    # Flood fill the grid
    queue = {(-1, 1)}  # We know this is outside the loop
    while queue:
        (x, y) = queue.pop()
        grid2[(x, y)] = "░"
        for neighbour in [
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
            (x, y - 1),
        ]:
            if neighbour in grid2:
                pass
            elif not 0 <= neighbour[0] <= width * 2 + 2:
                pass
            elif not 0 <= neighbour[1] <= height * 2 + 2:
                pass
            else:
                queue.add(neighbour)

    return len(
        [
            (x, y)
            for x in range(1, width * 2 + 2, 2)
            for y in range(1, height * 2 + 2, 2)
            if (x, y) not in grid2
        ]
    )


def main():
    lines = read_input()
    grid = parse_grid(lines)
    start = find_start(grid)

    part_1 = do_part_1(grid, start)
    print(f"{part_1=}")

    part_2 = do_part_2(lines, grid, start)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day10.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
