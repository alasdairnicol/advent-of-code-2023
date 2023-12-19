#!/usr/bin/env python
from collections import deque
from dataclasses import dataclass
import math
import operator
from typing import Callable, Type

Operator = Callable[[int, int], bool]
Condition = tuple[tuple[Operator, int], ...]
Conditions = tuple[Condition, Condition, Condition, Condition]

STARTING_WORKFLOW = "in"

operators = {
    "<": operator.lt,
    ">": operator.gt,
}


@dataclass
class Workflow:
    field: str
    op: Operator
    value: int
    accept: str | Type["Workflow"]
    reject: str | Type["Workflow"]

    @classmethod
    def from_str(cls, workflow_str: str):
        field = workflow_str[0]
        op = operators[workflow_str[1]]
        value_str, rest = workflow_str[2:].split(":", maxsplit=1)
        value = int(value_str)
        accept, reject_str = rest.split(",", maxsplit=1)
        reject = Workflow.from_str(reject_str) if ":" in reject_str else reject_str
        return Workflow(
            field=field,
            op=op,
            value=value,
            accept=accept,
            reject=reject,
        )

    def run(self, part: dict[str, int]) -> str | Type["Workflow"]:
        if self.op(part[self.field], self.value):
            return self.accept
        else:
            return self.reject

    @property
    def inverse_op(self):
        return {
            operator.lt: operator.ge,
            operator.gt: operator.le,
        }[self.op]


def parse_part(part_str: str) -> dict[str, int]:
    return {k: int(v) for k, v in (kv.split("=") for kv in part_str[1:-1].split(","))}


def parse_parts(parts_str: str) -> list[dict[str, int]]:
    return [parse_part(part_str) for part_str in parts_str.strip().split("\n")]


def parse_workflows(workflows_str):
    workflows = {}
    for named_workflow_str in workflows_str.strip().split("\n"):
        name, workflow_str = named_workflow_str[:-1].split("{")
        workflows[name] = Workflow.from_str(workflow_str)
    return workflows


def process_part(workflows: dict[str, Type["Workflow"]], part: dict[str, int]) -> bool:
    """
    Determines whether a given part is accepted or rejects
    """
    wf: str | Type["Workflow"] = STARTING_WORKFLOW
    while True:
        if isinstance(wf, str):
            if wf == "A":
                return True
            elif wf == "R":
                return False
            else:
                wf = workflows[wf]
        assert isinstance(wf, Workflow)
        wf = wf.run(part)


def num_parts_matching_conditions(conditions) -> list[int]:
    """
    Returns a list of integers [x, m, a, s] where each integer is the
    number of possible values for that letter than match the conditions.

    It would be more efficient to combine the conditions, e.g (x > 10, x > 20)
    can be reduced to (x > 20). But since the range is 1-4000, looping through
    the entire range and checking all the conditions is fast enough and finishes
    in under 3.5s.
    """
    return [
        len([x for x in range(1, 4001) if all(yy[0](x, yy[1]) for yy in y)])
        for y in conditions
    ]


def process_workflow(workflow: Workflow, conditions) -> list[tuple]:
    """
    Takes a workflow that applies to certain conditions,
    and splits it into two separate workflows with their
    own conditions.
    """
    conditions_dict = dict(zip("xmas", conditions))

    accept_dict = conditions_dict.copy()
    reject_dict = conditions_dict.copy()

    accept_dict[workflow.field] += ((workflow.op, workflow.value),)
    reject_dict[workflow.field] += ((workflow.inverse_op, workflow.value),)

    return [
        (workflow.accept, tuple(accept_dict.values())),
        (workflow.reject, tuple(reject_dict.values())),
    ]


def do_part_1(workflows, parts) -> int:
    return sum(sum(part.values()) for part in parts if process_part(workflows, part))


def do_part_2(workflows) -> int:
    initial_conditions = tuple(() for _ in "xmas")
    queue = deque([("in", initial_conditions)])

    accepted_conditions = []

    while queue:
        wf, conditions = queue.popleft()
        if isinstance(wf, str):
            if wf == "R":
                continue
            elif wf == "A":
                accepted_conditions.append(conditions)
                continue
            else:
                wf = workflows[wf]

        assert isinstance(wf, Workflow)
        for wf, conditions in process_workflow(wf, conditions):
            queue.append((wf, conditions))

    return sum(
        math.prod(num_parts_matching_conditions(conditions))
        for conditions in accepted_conditions
    )


def main():
    workflows_str, parts_str = read_input()
    workflows = parse_workflows(workflows_str)
    parts = parse_parts(parts_str)

    part_1 = do_part_1(workflows, parts)
    print(f"{part_1=}")

    part_2 = do_part_2(workflows)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day19.txt") as f:
        return f.read().split("\n\n")


if __name__ == "__main__":
    main()
