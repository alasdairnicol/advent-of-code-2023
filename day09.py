#!/usr/bin/env python
import itertools


def next_number(numbers: list[int]) -> int:
    diffs = [y - x for x, y in itertools.pairwise(numbers)]
    if all(x == 0 for x in diffs):
        return numbers[-1]
    else:
        return numbers[-1] + next_number(diffs)


def do_part_1(numbers_list: list[list[int]]) -> int:
    return sum(next_number(numbers) for numbers in numbers_list)


def do_part_2(numbers_list: list[list[int]]) -> int:
    # Same as part 1 but reverse numbers
    return sum(next_number(numbers[::-1]) for numbers in numbers_list)


def main():
    lines = read_input()
    numbers_list = [[int(x) for x in line.split()] for line in lines]

    part_1 = do_part_1(numbers_list)
    print(f"{part_1=}")

    part_2 = do_part_2(numbers_list)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day09.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
