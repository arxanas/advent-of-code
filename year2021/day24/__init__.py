import sys
from typing import List, Optional, Tuple

Input = List[Tuple[str, ...]]


def speculate_inputs(instructions: Input, digits: List[int]) -> bool:
    digits = list(digits)

    possible_values = {
        "w": {0},
        "x": {0},
        "y": {0},
        "z": {0},
    }

    def get_reg_values(key: str):
        if key in possible_values:
            return possible_values[key]
        else:
            return {int(key)}

    def cross_op(lhs_reg, rhs_reg, f):
        new_possible_values = set()
        for lhs in possible_values[lhs_reg]:
            for rhs in get_reg_values(rhs_reg):
                new_possible_values.add(f(lhs, rhs))
        possible_values[lhs_reg] = new_possible_values

    def mod(lhs, rhs):
        lhs %= rhs
        while lhs < 0:
            lhs += rhs
        return lhs

    for (i, instr) in enumerate(instructions):
        cmd = instr[0]
        if cmd == "inp":
            if digits:
                possible_values[instr[1]] = {digits.pop(0)}
            else:
                possible_values[instr[1]] = set(range(9, 0, -1))
        elif cmd == "add":
            cross_op(instr[1], instr[2], lambda x, y: x + y)
        elif cmd == "mul":
            cross_op(instr[1], instr[2], lambda x, y: x * y)
        elif cmd == "sub":
            cross_op(instr[1], instr[2], lambda x, y: x - y)
        elif cmd == "div":
            cross_op(instr[1], instr[2], lambda x, y: x // y)
        elif cmd == "mod":
            cross_op(instr[1], instr[2], mod)
        elif cmd == "eql":
            cross_op(instr[1], instr[2], lambda x, y: int(x == y))

        if any(len(x) == 0 for x in possible_values.values()):
            raise ValueError(f"Unsatisfiable: {possible_values}")

    return 0 in possible_values["z"]


def test_speculate_inputs() -> None:
    assert speculate_inputs(
        [
            ("inp", "w"),
        ],
        digits=[0],
    )
    assert not speculate_inputs(
        [
            ("inp", "w"),
            ("add", "z", "w"),
        ],
        digits=[1],
    )
    assert not speculate_inputs(
        [
            ("inp", "w"),
            ("inp", "x"),
            ("add", "z", "x"),
        ],
        digits=[1],
    )
    assert speculate_inputs(
        [
            ("inp", "w"),
            ("inp", "x"),
            ("add", "z", "-1"),
            ("add", "z", "x"),
        ],
        digits=[1],
    )


def search(instructions: Input, digits: List[int]) -> Optional[List[int]]:
    print("Trying with digits:", "".join(str(d) for d in digits))
    if len(digits) >= 14:
        return digits

    for i in range(9, 0, -1):
        if not speculate_inputs(instructions, digits=digits + [i]):
            continue
        result = search(instructions, digits=digits + [i])
        if result is not None:
            return result
    return None


def search2(instructions: Input, digits: List[int]) -> Optional[List[int]]:
    if len(digits) == 5:
        print("Trying with digits:", "".join(str(d) for d in digits))
    if len(digits) >= 14:
        return digits

    for i in range(1, 10):
        if not speculate_inputs(instructions, digits=digits + [i]):
            continue
        result = search2(instructions, digits=digits + [i])
        if result is not None:
            return result
    return None


def main() -> None:
    instructions = []
    for line in sys.stdin:
        words = line.split()
        instructions.append(tuple(words))

    # Very slow, could be multithreaded, but a better solution would probably
    # just be faster.
    print(search(instructions, digits=[]))
    print(search2(instructions, digits=[]))


if __name__ == "__main__":
    main()
