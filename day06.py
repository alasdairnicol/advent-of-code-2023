#!/usr/bin/env python
import math


def find_quadratic_roots(a, b, c):
    zero_1 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    zero_2 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    return (zero_1, zero_2)


def do_part_1(lines: list[str]) -> int:
    pairs = list(zip(*([int(x) for x in line.split(":")[1].split()] for line in lines)))
    return math.prod(
        len([distance for i in range(time) if (distance := (time - i) * i) > record])
        for time, record in pairs
    )


def do_part_2(lines: list[str]) -> int:
    time, distance = (int("".join(line.split(":")[1].split())) for line in lines)
    z1, z2 = find_quadratic_roots(a=1, b=-time, c=distance)
    if z1 == int(z1):
        z1 += 1
        z2 -= 1
    else:
        z1 = math.ceil(z1)
        z2 = math.floor(z2)

    return z2 - z1 + 1


def main():
    lines = read_input()

    part_1 = do_part_1(lines)
    print(f"{part_1=}")

    part_2 = do_part_2(lines)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day06.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
