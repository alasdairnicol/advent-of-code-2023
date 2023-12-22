#!/usr/bin/env python
# x,y,z points
Point = tuple[int, int, int]
# maps a brick_id (int) to a list of points
Bricks = dict[int, list[Point]]
# maps a Point to the brick_id that occupies that point
Grid = dict[Point, int]


def parse_bricks(lines: list[str]) -> Bricks:
    """
    For each brick, we only store the positions that the brick
    occupies. If we stored the other bricks that each brick
    supports/is supported by, then we'd be able to tell whether
    bricks can drop more efficiently, rather than having to test
    every point below each brick.
    """
    bricks = {}
    for i, line in enumerate(lines, 1):
        start, end = line.strip().split("~")
        xs, ys, zs = (int(x) for x in start.split(","))
        xe, ye, ze = (int(x) for x in end.split(","))
        positions = [
            (x, y, z)
            for x in range(xs, xe + 1)
            for y in range(ys, ye + 1)
            for z in range(zs, ze + 1)
        ]
        bricks[i] = positions

    return bricks


def create_grid(bricks: Bricks) -> dict[Point, int]:
    grid = {}
    for brick_id, points in bricks.items():
        for point in points:
            grid[point] = brick_id

    return grid


def add_floor(grid: Grid) -> None:
    """
    Adds a floor at z=0.

    Modifies grid
    """
    x_min = min(x for x, y, z in grid)
    x_max = max(x for x, y, z in grid)
    y_min = min(y for x, y, z in grid)
    y_max = max(y for x, y, z in grid)

    # Add the floor
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            grid[x, y, 0] = 0


def lowest_z(positions: list[Point]) -> int:
    """The minimum level occupied by that brick"""
    return min(z for x, y, z in positions)


def ordered_bricks(bricks: Bricks) -> list[int]:
    """
    Return a list of brick_ids, ordered from lowest to highest
    """
    return sorted(bricks, key=lambda x: lowest_z(bricks[x]))


def drop_brick(grid: Grid, bricks: Bricks, brick_id: int) -> bool:
    """
    Drop a brick as far as it will go.

    Modifies grid and bricks

    Returns a bool that indicates whether the brick dropped at least one level
    """
    positions = bricks[brick_id]
    dropped = False
    while True:
        dropped_positions = [(x, y, z - 1) for x, y, z in positions]
        if all(grid.get(p, brick_id) == brick_id for p in dropped_positions):
            dropped = True
            for p in positions:
                del grid[p]
            positions = dropped_positions
            bricks[brick_id] = dropped_positions
            for p in positions:
                grid[p] = brick_id
        else:
            break
    return dropped


def drop_bricks(grid: Grid, bricks: Bricks) -> int:
    """
    Drop the bricks as far as they will go

    Modifies grid and bricks
    """
    return sum(
        1 if drop_brick(grid, bricks, brick_id) else 0
        for brick_id in sorted(bricks, key=lambda x: lowest_z(bricks[x]))
    )


def remove_brick(grid, bricks, brick_id) -> int:
    """
    Calculate the number of bricks that would fall if we
    removed brick_id
    """
    grid = {k: v for k, v in grid.items() if v != brick_id}
    bricks = {k: v for k, v in bricks.items() if k != brick_id}

    return sum(
        1 if drop_brick(grid, bricks, brick_id) else 0
        for brick_id in sorted(bricks, key=lambda x: lowest_z(bricks[x]))
    )


def main():
    lines = [line.strip() for line in read_input()]

    bricks = parse_bricks(lines)
    grid = create_grid(bricks)
    add_floor(grid)

    drop_bricks(grid, bricks)

    num_dropped = {
        brick_id: remove_brick(grid, bricks, brick_id) for brick_id in bricks
    }

    part_1 = len([k for k, v in num_dropped.items() if not v])
    part_2 = sum(num_dropped.values())

    print(f"{part_1=}")
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day22.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
