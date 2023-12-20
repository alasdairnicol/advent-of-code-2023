#!/usr/bin/env python
from collections import defaultdict, deque
import math
from typing import cast


def parse_lines(lines):
    destinations = {}
    types = {}
    flipflops = {}
    inputs = defaultdict(dict)

    for line in lines:
        module, destinations_str = line.strip().split(" -> ")
        destination_names = destinations_str.split(", ")
        module_type = module  # catches 'broadcaster' case
        if module.startswith("%"):
            module_type = "flipflop"
            name = module[1:]
            flipflops[name] = False
        elif module.startswith("&"):
            module_type = "conjunction"
            name = module[1:]
        else:
            name = module
        types[name] = module_type
        destinations[name] = destination_names

        for destination in destination_names:
            inputs[destination][name] = False

    destinations["button"] = "broadcaster"
    types["button"] = "button"

    return (destinations, flipflops, inputs, types)


def process_pulses(destinations, flipflops, inputs, types, pulses):
    low = 0
    high = 0

    output_false = set()

    while pulses:
        name, source, value = pulses.popleft()
        if value:
            high += 1
        else:
            low += 1

        module_type = types.get(name)
        if module_type == "button":
            # Single low pulse from button to broadcaster
            pulses.append(("broadcaster", "button", False))
        elif module_type == "broadcaster":
            for dest in destinations["broadcaster"]:
                pulses.append((dest, "broadcaster", value))
        elif module_type == "flipflop":
            if value:
                pass
            else:
                # low pulse flips value
                flipflops[name] = not flipflops[name]
                for dest in destinations[name]:
                    pulses.append((dest, name, flipflops[name]))
        elif module_type == "conjunction":
            if name in ("gc", "sz", "cm", "xf") and not value:
                output_false.add(name)
            inputs[name][source] = value
            value = not all(inputs[name].values())
            for dest in destinations[name]:
                pulses.append((dest, name, value))
        else:
            pass
    return low, high, output_false


def do_part_1(lines) -> int:
    destinations, flipflops, inputs, types = parse_lines(lines)

    total_low = 0
    total_high = 0
    pulses: deque = deque()

    for i in range(1000):
        # destination, source, value
        pulses.append(
            ("broadcaster", "button", False),
        )
        low, high, _ = process_pulses(destinations, flipflops, inputs, types, pulses)
        total_low += low
        total_high += high
    return total_low * total_high


def do_part_2(lines) -> int:
    destinations, flipflops, inputs, types = parse_lines(lines)

    pulses: deque = deque()
    nodes: dict[str, int | None] = {"gc": None, "sz": None, "cm": None, "xf": None}
    count = 0

    while not all(nodes.values()):
        # destination, source, value
        pulses.append(
            ("broadcaster", "button", False),
        )
        count += 1

        _, __, output_false = process_pulses(
            destinations, flipflops, inputs, types, pulses
        )
        for name in output_false:
            if not nodes[name]:
                nodes[name] = count

    node_values = cast(list[int], list(nodes.values()))
    return math.prod(node_values)


def main():
    lines = read_input()

    part_1 = do_part_1(lines)
    print(f"{part_1=}")

    part_2 = do_part_2(lines)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day20.txt") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
