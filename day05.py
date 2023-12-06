#!/usr/bin/env python


def parse_mappings(mapping_blocks):
    mappings = []
    for block in mapping_blocks:
        mapping = {}
        for line in block.strip().split("\n")[1:]:
            destination, source, length = (int(x) for x in line.split())
            mapping[range(source, source + length)] = destination - source
        mappings.append(mapping)
    return mappings


def combine_ranges(old_range, new_range, delta):
    out = []

    overlap = range(
        max(old_range.start, new_range.start), min(old_range.stop, new_range.stop)
    )

    before = range(old_range.start, min(overlap.start, old_range.stop))
    after = range(max(overlap.stop, old_range.start), old_range.stop)

    if overlap:
        overlap = range(overlap.start + delta, overlap.stop + delta)
    else:
        overlap = None
    leftover = set()
    if before:
        leftover.add(before)
    if after:
        leftover.add(after)
    if overlap:
        out.append(range(overlap.start + delta, overlap.stop + delta))
    return overlap, leftover


def find_lowest_location(mappings, ranges):
    for mapping in mappings:
        next_round = set()
        for key, delta in mapping.items():
            old_ranges = list(ranges)
            ranges = set()
            for r in old_ranges:
                overlap, leftover = combine_ranges(r, key, delta)
                if overlap:
                    next_round.add(overlap)
                ranges |= leftover  # rename leftover_ranges???

        ranges = next_round | ranges

    return min(r.start for r in ranges)


def main():
    blocks = read_input()

    seed_numbers = [int(x) for x in blocks[0].split(":")[1].split()]

    seeds_part_1 = [range(x, x + 1) for x in seed_numbers]

    seeds_part_2 = []

    for i in range(0, len(seed_numbers), 2):
        seeds_part_2.append(
            range(seed_numbers[i], seed_numbers[i] + seed_numbers[i + 1])
        )

    mappings = parse_mappings(blocks[1:])

    part_1 = find_lowest_location(mappings, seeds_part_1)
    print(f"{part_1=}")

    part_2 = find_lowest_location(mappings, seeds_part_2)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day05.txt") as f:
        return f.read().split("\n\n")


if __name__ == "__main__":
    main()
