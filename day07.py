#!/usr/bin/env python
from collections import Counter

values = {k: v for v, k in enumerate("23456789TJQKA", 2)}


class Hand:
    def __init__(self, cards, bid):
        self.cards = [values[c] for c in cards]
        self.bid = int(bid)
        self.jokers_low = [c if c != 11 else 1 for c in self.cards]

    def __str__(self):
        return f"{self.cards} {self.bid}"

    def strength(self, jokers=False):
        counter = Counter(self.cards)

        if jokers:
            num_jacks = counter[values["J"]]
            if 1 <= num_jacks <= 4:
                counter.pop(values["J"])
                counter.update({counter.most_common()[0][0]: num_jacks})

        most_common = counter.most_common()

        if most_common[0][1] == 5:
            return 100  # five of a kind
        elif most_common[0][1] == 4:
            return 90  # four of a kind
        elif most_common[0][1] == 3 and most_common[1][1] == 2:
            return 80  # full house
        elif most_common[0][1] == 3:
            return 70  # three of a kind
        elif most_common[0][1] == 2 and most_common[1][1] == 2:
            return 60  # two pair
        elif most_common[0][1] == 2:
            return 50  # one pair
        return 40


def score_hands(hands: list[Hand]) -> int:
    return sum(h.bid * i for i, h in enumerate(hands, 1))


def do_part_1(hands: list[Hand]) -> int:
    hands.sort(key=lambda h: (h.strength(), h.cards))
    return score_hands(hands)


def do_part_2(hands: list[Hand]) -> int:
    hands.sort(key=lambda h: (h.strength(jokers=True), h.jokers_low))
    return sum(h.bid * i for i, h in enumerate(hands, 1))


def main():
    lines = read_input()
    hands = [Hand(card, bid) for card, bid in (line.split() for line in lines)]

    part_1 = do_part_1(hands)
    print(f"{part_1=}")

    part_2 = do_part_2(hands)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day07.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
