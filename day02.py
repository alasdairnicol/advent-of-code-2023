#!/usr/bin/env python
import math


def do_part_1(lines: list[str]) -> int:
    bag = {"red": 12, "green": 13, "blue": 14}

    total = 0
    for i, line in enumerate(lines, 1):
        grabs = line.split(":")[1].split(";")
        if all(
            all(
                bag[y] >= int(x)
                for x, y in (draw.strip().split(" ") for draw in grab.split(","))
            )
            for grab in grabs
        ):
            total += i
    return total


def do_part_2(lines: list[str]) -> int:
    bag = {"red": 12, "green": 13, "blue": 14}
    total = 0
    for i, line in enumerate(lines, 1):
        grabs = line.split(":")[1].split(";")

        grab_dicts = [
            {
                v: int(k)
                for k, v in [draw.strip().split(" ") for draw in grab.split(",")]
            }
            for grab in grabs
        ]
        minimums = {}
        for colour in bag:
            minimums[colour] = max(d.get(colour, 0) for d in grab_dicts)
        total += math.prod(minimums.values())
    return total


def main():
    lines = read_input()

    part_1 = do_part_1(lines)
    print(f"{part_1=}")

    part_2 = do_part_2(lines)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day02.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
