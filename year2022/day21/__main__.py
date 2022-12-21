import sys
from typing import Union

import z3  # type: ignore

TEST_INPUT = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

PART_1_ANSWER = 152
PART_2_ANSWER = 301

Instr = Union[int, tuple[str, str, str]]

Input = dict[str, Instr]


def parse_input(input: str) -> Input:
    result: dict[str, Instr] = {}
    for line in input.strip().splitlines():
        name, instr = line.split(": ")
        if instr.isnumeric():
            result[name] = int(instr)
        else:
            (lhs, op, rhs) = instr.split(" ")
            result[name] = (lhs, op, rhs)
    return result


def part1(input: Input) -> int:
    solver = z3.Solver()
    vars = {name: z3.Int(name) for name in input}
    for name, instr in input.items():
        match instr:
            case int(value):
                solver.add(vars[name] == value)
            case (lhs, "+", rhs):
                solver.add(vars[name] == vars[lhs] + vars[rhs])
            case (lhs, "-", rhs):
                solver.add(vars[name] == vars[lhs] - vars[rhs])
            case (lhs, "*", rhs):
                solver.add(vars[name] == vars[lhs] * vars[rhs])
            case (lhs, "/", rhs):
                solver.add(vars[name] == vars[lhs] / vars[rhs])
            case instr:
                raise ValueError(f"unknown instruction {instr}")
    assert solver.check() == z3.sat
    model = solver.model()
    root = model[vars["root"]]
    assert isinstance(root, z3.IntNumRef)
    return root.as_long()


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    solver = z3.Solver()
    vars = {name: z3.Int(name) for name in input}
    for name, instr in input.items():
        match (name, instr):
            case ("root", (lhs, _, rhs)):
                # Add two separate constraints for debuggability.
                solver.add(vars["root"] == (vars[lhs] == vars[rhs]))
                solver.add(vars["root"] == 1)
            case ("humn", instr):
                # Leave the `humn` variable unbound.
                assert isinstance(instr, int)
            case (name, int(value)):
                solver.add(vars[name] == value)
            case (name, (lhs, "+", rhs)):
                solver.add(vars[name] == vars[lhs] + vars[rhs])
            case (name, (lhs, "-", rhs)):
                solver.add(vars[name] == vars[lhs] - vars[rhs])
            case (name, (lhs, "*", rhs)):
                solver.add(vars[name] == vars[lhs] * vars[rhs])
            case (name, (lhs, "/", rhs)):
                # There may be multiple solutions if we use integer division, so
                # restrict the constraints such that lhs / rhs is an integer.
                # Otherwise, we may get multiple solutions; see
                # https://www.reddit.com/r/adventofcode/comments/zrbw7n/2022_day_21_part_2_solution_not_unique/
                solver.add(
                    vars[name] == vars[lhs] / vars[rhs], vars[lhs] % vars[rhs] == 0
                )
            case (name, instr):
                raise ValueError(f"unknown instruction {name}: {instr}")
    assert solver.check() == z3.sat
    model = solver.model()
    humn = model[vars["humn"]]
    assert isinstance(humn, z3.IntNumRef)
    return humn.as_long()


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
