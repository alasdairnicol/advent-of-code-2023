#!/usr/bin/env python
from functools import cache
import itertools


def count_valid_combinations(conditions: str, numbers: tuple[int, ...]) -> int:
    """
    Calculates how many of the remaining '?' should be '#'
    then iterates through all the combinations, counting how
    many are valid arrangements.

    This was fast enough to do part 1 in under 2 seconds, but far too slow to
    use to brute force part 2.
    """
    num_damaged = sum(numbers)
    known_damaged = conditions.count("#")
    unknowns = [i for i, c in enumerate(conditions) if c == "?"]
    num_unknown_damaged = num_damaged - known_damaged

    count = 0
    for trial_damaged in itertools.combinations(unknowns, num_unknown_damaged):
        trial = "".join(
            "#" if c == "#" or i in trial_damaged else "."
            for i, c in enumerate(conditions)
        )
        arrangements = tuple(len(word) for word in trial.split(".") if word)
        if arrangements == numbers:
            count += 1
    return count


@cache
def count_ways_recursively(conditions: str, numbers: tuple[int, ...]) -> int:
    """
    Count the number of ways recursively using caching

    This is a bit ugly. There's some duplication between the
    elif conditions[0] == "#": and final else branch.

    We could probably detect invalid states where we can terminate earlier,
    but because we are using a cache the current checks are fast enough for
    the size of the problem input.
    """
    # End conditions
    if not numbers:
        # Not valid if we used up all the numbers and there
        # are still # remaining
        return 0 if "#" in conditions else 1
    if not conditions:
        # Not valid if we reached the end of the string and there
        # are still numbers remaining
        return 0 if numbers else 1

    if conditions[0] == ".":
        return count_ways_recursively(conditions[1:], numbers)

    elif conditions[0] == "#":
        # Will the next group fit here?
        if conditions[: numbers[0]].replace("?", "#") != "#" * numbers[0]:
            return 0
        elif len(numbers) > 1:
            if len(conditions) < numbers[0] + 1:
                # The remaining string is too short
                return 0
            elif conditions[numbers[0]] == "#":
                # The next group is too long
                return 0
        return count_ways_recursively(conditions[numbers[0] + 1 :], numbers[1:])
    else:
        # Count ways assuming conditions starts with '#'
        if conditions[: numbers[0]].replace("?", "#") != "#" * numbers[0]:
            a = 0
        elif len(numbers) > 1:
            if len(conditions) < numbers[0] + 1:
                a = 0
            elif conditions[numbers[0]] == "#":
                a = 0
            else:
                a = count_ways_recursively(conditions[numbers[0] + 1 :], numbers[1:])
        else:
            # final number
            a = 0 if "#" in conditions[numbers[0] :] else 1

        # count ways assuming conditions starts with a '.'
        b = count_ways_recursively(conditions[1:], numbers)

        return a + b


def parse_line(line: str, multiplier: int = 1) -> tuple[str, tuple[int, ...]]:
    conditions, number_str = line.split()
    numbers = tuple(int(x) for x in number_str.split(","))

    if multiplier != 1:
        conditions = "?".join([conditions] * multiplier)
        numbers = numbers * multiplier

    return conditions, numbers


def do_part_1(lines: str) -> int:
    # original approach
    # return sum(count_valid_combinations(*parse_line(line)) for line in lines)
    return sum(count_ways_recursively(*parse_line(line)) for line in lines)


def do_part_2(lines: str) -> int:
    return sum(
        count_ways_recursively(*parse_line(line, multiplier=5)) for line in lines
    )


def main():
    lines = read_input()
    part_1 = do_part_1(lines)
    print(f"{part_1=}")

    part_2 = do_part_2(lines)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day12.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
