#!/usr/bin/env python


def extract_digits(line: str) -> int:
    digits = [x for x in line if x.isdigit()]
    return int(f"{digits[0]}{digits[-1]}")


def do_part_1(lines: list[str]) -> int:
    return sum(extract_digits(line) for line in read_input())


numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def extract_digits_and_words(line):
    first_digit = None
    last_digit = None
    for i, x in enumerate(line):
        digit = None
        if x.isdigit():
            digit = x
        else:
            for j, number in enumerate(numbers, 1):
                if line[i:].startswith(number):
                    digit = j
                    break
        if digit is not None:
            if first_digit is None:
                first_digit = digit
            last_digit = digit
    return int(f"{first_digit}{last_digit}")


def do_part_2(lines: list[str]) -> int:
    return sum(extract_digits_and_words(line) for line in read_input())


def main():
    lines = read_input()

    part_1 = do_part_1(lines)
    print(f"{part_1=}")

    part_2 = do_part_2(lines)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day01.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
