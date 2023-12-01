import sys
from collections import Counter
from typing import Dict, List


def simulate_lanternfish(fishes: List[int]) -> List[int]:
    result = []
    for fish in fishes:
        if fish == 0:
            result.append(8)
            result.append(6)
        else:
            result.append(fish - 1)
    return result


def simx(fishes: List[int], x: int) -> List[int]:
    for i in range(x):
        fishes = simulate_lanternfish(fishes)
    return fishes


def simulate_lanternfish2(fishes: Dict[int, int]) -> Dict[int, int]:
    result: Counter[int] = Counter()
    for fish, count in fishes.items():
        if fish == 0:
            result[8] += count
            result[6] += count
        else:
            result[fish - 1] += count
    return result


def simx2(fishes: Dict[int, int], x: int) -> Dict[int, int]:
    for i in range(x):
        fishes = simulate_lanternfish2(fishes)
    return fishes


def main() -> None:
    test = [3, 4, 3, 1, 2]
    print("test 1 (18 days):", len(simx(test, 18)))
    print("test 1 (80 days):", len(simx(test, 80)))
    test2 = Counter([3, 4, 3, 1, 2])
    print("test 2:", sum(simx2(test2, 256).values()))

    fishes = [int(x) for x in sys.stdin.read().strip().split(",")]
    print("part 1:", len(simx(fishes, 80)))

    fishes2 = Counter(fishes)
    print("part 2:", sum(simx2(fishes2, 256).values()))


if __name__ == "__main__":
    main()
