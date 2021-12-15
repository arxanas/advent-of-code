import sys
from typing import List


def helper(x):
    return (x * (x + 1)) // 2


def main() -> None:
    crabs = [int(i) for i in sys.stdin.read().strip().split(",")]
    end = max(crabs)

    print(
        "part 1:",
        min(sum(abs(target - crab) for crab in crabs) for target in range(end + 1)),
    )
    print(
        "part 2:",
        min(
            sum(helper(abs(target - crab)) for crab in crabs)
            for target in range(end + 1)
        ),
    )


if __name__ == "__main__":
    main()
