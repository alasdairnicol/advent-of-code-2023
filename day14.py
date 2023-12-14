#!/usr/bin/env python

Rows = tuple[tuple[str, ...], ...]
Columns = tuple[tuple[str, ...], ...]


def parse_lines(lines: list[str]) -> Rows | Columns:
    return tuple(tuple(line.strip()) for line in lines)


def sort_line(line, reverse):
    return "#".join(
        "".join(sorted(part, reverse=reverse)) for part in "".join(line).split("#")
    )


def score_column(column: tuple[str, ...]) -> int:
    return sum(i for i, x in enumerate(reversed(column), 1) if x == "O")


def tilt_north(rows: Rows) -> Columns:
    return tuple(sort_line(col, reverse=True) for col in zip(*rows))


def tilt_west(columns: Columns) -> Rows:
    return tuple(sort_line(row, reverse=True) for row in zip(*columns))


def tilt_south(rows: Rows) -> Columns:
    return tuple(sort_line(col, reverse=False) for col in zip(*rows))


def tilt_east(columns: Columns) -> Rows:
    return tuple(sort_line(row, reverse=False) for row in zip(*columns))


def spin_cycle(rows):
    columns = tilt_north(rows)
    rows = tilt_west(columns)
    columns = tilt_south(rows)
    return tilt_east(columns)


def do_part_1(rows: Rows) -> int:
    return sum(score_column(c) for c in tilt_north(rows))


def do_part_2(rows: Rows) -> int:
    seen = {}
    count = 0

    while True:
        if rows in seen:
            break
        else:
            seen[rows] = count

        rows = spin_cycle(rows)
        count += 1

    total_spins = 1_000_000_000
    cycle_length = count - seen[rows]

    remainder = (total_spins - count) % cycle_length

    for _ in range(remainder):
        rows = spin_cycle(rows)

    return sum(score_column(c) for c in zip(*rows))


def main():
    lines = read_input()
    rows = parse_lines(lines)

    part_1 = do_part_1(rows)
    print(f"{part_1=}")

    part_2 = do_part_2(rows)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day14.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
