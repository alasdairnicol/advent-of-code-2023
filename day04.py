#!/usr/bin/env python
import functools


def card_score(line: str) -> int:
    return len(
        functools.reduce(
            lambda a, b: a & b,
            ({int(x) for x in part.split()} for part in line.split(":")[1].split("|")),
        )
    )


def do_part_1(scores: list[int]) -> int:
    return sum(2 ** (s - 1) if s else 0 for s in scores)


def do_part_2(scores: list[int]) -> int:
    num_cards = {x: 1 for x in range(1, len(scores) + 1)}
    for i, score in enumerate(scores, 1):
        for x in range(i + 1, i + 1 + score):
            num_cards[x] += num_cards[i]

    return sum(num_cards.values())


def main():
    lines = read_input()
    scores = [card_score(line) for line in lines]

    part_1 = do_part_1(scores)
    print(f"{part_1=}")

    part_2 = do_part_2(scores)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day04.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
