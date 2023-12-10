#!/usr/bin/env python
def parse_grid(lines: list[int]) -> dict[tuple[int, int], str]:
    grid = {}
    for j, line in enumerate(lines):
        for i, val in enumerate(line):
            if val != ".":
                grid[(i, j)] = val
    return grid


def find_neighbour(grid, start_point):
    for direction, shapes in [
        ((1, 0), {"-", "J", "7"}),
        ((0, 1), {"|", "L", "J"}),
        ((-1, 0), {"-", "F", "L"}),
        ((0, -1), {"|", "7", "F"}),
    ]:
        neighbour = (start_point[0] + direction[0], start_point[1] + direction[1])
        if grid[neighbour] in shapes:
            return neighbour, direction


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
    point, direction = find_neighbour(grid, start)
    count = 1
    while point != start:
        point, direction = next_point(grid, point, direction)
        count += 1
    return count // 2


def main():
    lines = read_input()
    grid = parse_grid(lines)
    start = find_start(grid)

    part_1 = do_part_1(grid, start)
    print(f"{part_1=}")


def read_input() -> list[str]:
    with open("day10.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
