#!/usr/bin/env python
from typing import Sequence, Iterable


def num_differences(line1, line2):
    return len([1 for (x, y) in zip(line1, line2) if x != y])


def test_mirror(lines: Sequence[Iterable], test_line: int, num_smudges=0) -> bool:
    above = range(test_line, -1, -1)
    below = range(test_line + 1, len(lines))
    return (
        sum(num_differences(lines[i], lines[j]) for i, j in zip(above, below))
        == num_smudges
    )


def find_mirror(lines: Sequence[Iterable], num_smudges: int = 0):
    for i in range(len(lines) - 1):
        # for (i,row_above),(j,row_below) in itertools.pairwise(enumerate(rows)):
        if test_mirror(lines, i, num_smudges=num_smudges):
            return i + 1  # rows and columns are 1-indexed in problem definition
    return 0


def pattern_summary(pattern: str, num_smudges: int = 0) -> int:
    rows = [line.strip() for line in pattern.split()]
    columns = list(zip(*rows))
    summary = find_mirror(rows, num_smudges=num_smudges) * 100 + find_mirror(
        columns, num_smudges=num_smudges
    )
    return summary


def do_part_1(patterns: list[str]) -> int:
    return sum(pattern_summary(pattern) for pattern in patterns)


def do_part_2(patterns: list[str]) -> int:
    return sum(pattern_summary(pattern, num_smudges=1) for pattern in patterns)


def main():
    patterns = read_input()
    part_1 = do_part_1(patterns)
    print(f"{part_1=}")

    part_2 = do_part_2(patterns)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day13.txt") as f:
        return f.read().split("\n\n")


if __name__ == "__main__":
    main()
