#!/usr/bin/env python
from functools import reduce

Box = dict[str, int]


def hash_value(value):
    return reduce(lambda x, y: (x + ord(y)) * 17 % 256, value, 0)


def box_focussing_power(box_number: int, box: Box):
    """The total focussing power of all the lenses in a box"""
    return sum(
        ((box_number + 1) * (lens_number) * value)
        for (lens_number, (k, value)) in enumerate(box.items(), 1)
    )


def do_part_1(steps: list[str]) -> int:
    return sum(hash_value(step) for step in steps)


def do_part_2(steps: list[str]) -> int:
    boxes: list[Box] = [{} for _ in range(256)]

    for step in steps:
        if step.endswith("-"):
            operation = "remove"
            lens = step[:-1]
            value = None
        elif "=" in step:
            operation = "place"
            lens, value_str = step.split("=")
            value = int(value_str)
        else:
            raise ValueError("Invalid operation")
        box_number = hash_value(lens)

        if operation == "remove":
            boxes[box_number].pop(lens, None)
        else:
            boxes[box_number][lens] = value
    return sum(box_focussing_power(n, box) for n, box in enumerate(boxes))


def main():
    input_str = read_input()
    steps = input_str.split(",")

    part_1 = do_part_1(steps)
    print(f"{part_1=}")

    part_2 = do_part_2(steps)
    print(f"{part_2=}")


def read_input() -> str:
    with open("day15.txt") as f:
        return f.read().strip()


if __name__ == "__main__":
    main()
