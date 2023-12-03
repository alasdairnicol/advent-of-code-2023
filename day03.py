#!/usr/bin/env python
from collections import defaultdict
from typing import Generator

Point = tuple[int, int]


def build_numbers(lines: list[str]) -> dict[Point, int]:
    """
    Returns a dictionary where the keys are the starting position
    of the number and the values are the value of the number.
    """
    numbers = {}
    for j, line in enumerate(lines):
        digits = []
        starting_point = None
        # add '.' to end of each line so that we reach the
        # end of any numbers in progress
        for i, char in enumerate(line.strip() + "."):
            if char.isdigit():
                if starting_point is None:
                    starting_point = (i, j)
                digits.append(line[i])
            else:
                if digits:
                    number = int("".join(digits))
                    assert starting_point is not None
                    numbers[starting_point] = number

                    # reset
                    digits = []
                    starting_point = None
    return numbers


def build_symbols(lines: list[str]) -> dict[Point, str]:
    """
    Returns a dictionary where the keys are the starting position
    of the symbol and the values are the symbol
    """
    symbols = {}
    for j, line in enumerate(lines):
        for i, char in enumerate(line.strip()):
            if char != ".":
                symbols[(i, j)] = char
    return symbols


def nearby_points(starting_point: Point, number: int) -> Generator[Point, None, None]:
    """
    Yields generator of points next to all the points adjacent to the number,
    including diagonally.
    """
    min_x = starting_point[0] - 1
    max_x = starting_point[0] + len(str(number))
    for x in range(min_x, max_x + 1):
        yield (x, starting_point[1] - 1)
        yield (x, starting_point[1] + 1)
    yield (min_x, starting_point[1])
    yield (max_x, starting_point[1])


def build_nearby_symbols(
    numbers: dict[Point, int], symbols: dict[Point, str]
) -> dict[Point, Point]:
    """
    Returns a dict where the keys are the starting points of the number
    and the values are Points of adjacent symbols.

    Note this approach assumes that each number is adjacent to zero or one symbol(s)
    """
    nearby_symbols = {}
    for starting_point, number in numbers.items():
        for point in nearby_points(starting_point, number):
            if point in symbols:
                nearby_symbols[starting_point] = point
    return nearby_symbols


def do_part_1(numbers: dict[Point, int], nearby_symbols) -> int:
    return sum(numbers[starting_point] for starting_point in nearby_symbols)


def do_part_2(
    numbers: dict[Point, int], symbols: dict[Point, str], nearby_symbols
) -> int:
    gears = defaultdict(list)

    for starting_point, symbol_point in nearby_symbols.items():
        if symbols[symbol_point] == "*":
            gears[symbol_point].append(numbers[starting_point])

    return sum([gear[0] * gear[1] for gear in gears.values() if len(gear) == 2])


def main():
    lines = read_input()

    numbers = build_numbers(lines)
    symbols = build_symbols(lines)
    nearby_symbols = build_nearby_symbols(numbers, symbols)

    part_1 = do_part_1(numbers, nearby_symbols)
    print(f"{part_1=}")

    part_2 = do_part_2(numbers, symbols, nearby_symbols)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day03.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
