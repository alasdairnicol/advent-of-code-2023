#!/usr/bin/env python
import math
import itertools

NodeChildren = dict[str, tuple[str, ...]]


def parse_input(input_str: str) -> tuple[NodeChildren, str]:
    instructions, nodes = input_str.strip().split("\n\n")
    node_children = {
        parent: tuple(children.split(", ", maxsplit=1))
        for parent, children in [
            node.replace("(", "").replace(")", "").split(" = ")
            for node in nodes.split("\n")
        ]
    }
    return node_children, instructions


def calc_length(
    node_children: NodeChildren, node: str, instructions: str
) -> tuple[int, str]:
    instructions_cycle = itertools.cycle(instructions)
    count = 0
    start = node
    while True:
        node = (
            node_children[node][0]
            if next(instructions_cycle) == "L"
            else node_children[node][1]
        )
        count += 1
        if node.endswith("Z"):
            if start.endswith("Z"):
                assert start == node
            break
    return count, node


def do_part_1(node_children, instructions) -> int:
    count, _ = calc_length(node_children, "AAA", instructions)
    return count


def do_part_2(node_children, instructions) -> int:
    node_lengths = {
        node: calc_length(node_children, node, instructions)
        for node in node_children
        if node.endswith("A") or node.endswith("Z")
    }

    # Check that if XXA -> XXZ in x steps, then XXZ -> XXZ in x steps as well
    for start, (length, dest) in node_lengths.items():
        if start.endswith("A"):
            next_length, next_dest = node_lengths[dest]
            assert length == next_length
            assert dest == next_dest

    # The assertions above means that the minimum number of steps is the LCM of
    # the lengths of the starting nodes
    lengths = (v[0] for k, v in node_lengths.items() if k.endswith("A"))
    return math.lcm(*lengths)


def main():
    input_str = read_input()
    node_children, instructions = parse_input(input_str)

    part_1 = do_part_1(node_children, instructions)
    print(f"{part_1=}")

    part_2 = do_part_2(node_children, instructions)
    print(f"{part_2=}")


def read_input() -> str:
    with open("day08.txt") as f:
        return f.read()


if __name__ == "__main__":
    main()
