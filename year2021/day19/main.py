import sys
from collections import *
from functools import *
from typing import *
from dataclasses import dataclass
import math

TEST_INPUT = """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""


Point = Tuple[int, int, int]
Input = List[List[Point]]

# destination tuple entry -> (negate, source tuple entry)
Orientation = Dict[int, Tuple[bool, int]]


def distance(lhs: Point, rhs: Point) -> int:
    return abs(lhs[0] - rhs[0]) + abs(lhs[1] - rhs[1]) + abs(lhs[2] - rhs[2])


def plus(lhs: Point, rhs: Point) -> Point:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1], lhs[2] + rhs[2])


def minus(lhs: Point, rhs: Point) -> Point:
    return (lhs[0] - rhs[0], lhs[1] - rhs[1], lhs[2] - rhs[2])


def orient(p11: Point, p12: Point, p21: Point, p22: Point) -> Orientation:
    """Given beacons p11 and p12 observed by scanner 1 and beacons p21 and p22
    observed by scanner 2, where these beacons are known to be the same,
    determine a transformation that would translate p21 into a coordinate system
    compatible with p1.
    """
    result = {}
    for i in range(3):
        # Start with a field `i` from scanner 1.
        d1 = p11[i] - p12[i]
        for j in range(3):
            # Look for a field `j` in scanner 2 which seems to be the same.
            d2 = p21[j] - p22[j]
            if abs(d1) == abs(d2):
                assert d1 != 0
                assert d2 != 0
                negate = (d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)

                # Field `j` should become field `i`.
                result[i] = (negate, j)
                break
    assert len(result) == 3
    return result


def apply_orientation(source: Point, orientation: Orientation) -> Point:
    result = []
    for i in range(3):
        (negate, index) = orientation[i]
        multiplier = -1 if negate else 1
        result.append(multiplier * source[index])
    assert len(result) == 3
    return tuple(result)


def invert_orientation(orientation: Orientation) -> Orientation:
    return {v[1]: (v[0], k) for (k, v) in orientation.items()}


def compose_orientation(o1: Orientation, o2: Orientation) -> Orientation:
    result = {}
    for (index1, v1) in o1.items():
        v2 = o2[v1[1]]
        index2 = v2[1]
        negate = v1[0] != v2[0]
        result[index1] = (negate, index2)
    return result


def test_orient() -> None:
    p11 = (2, 1, 0)
    p12 = (3, 3, 10)
    p21 = (1, 3, 0)
    p22 = (-1, 2, 10)
    o = orient(p11, p12, p21, p22)
    assert apply_orientation(p21, o) == (-3, -1, 0)

    assert compose_orientation(o, o) == {
        0: (False, 0),
        1: (False, 1),
        2: (False, 2),
    }


def problem(input: Input) -> object:
    scanner_locations = {
        0: (
            (0, 0, 0),
            {
                0: (False, 0),
                1: (False, 1),
                2: (False, 2),
            },
        ),
    }

    while len(scanner_locations) < len(input):
        for (i, scanner1) in enumerate(input):
            for (j, scanner2) in enumerate(input):
                if j == i or j in scanner_locations:
                    continue
                assert scanner1 != scanner2

                for beacon1 in scanner1:
                    edges1 = sorted(
                        [(distance(beacon1, x), x) for x in scanner1 if beacon1 != x]
                    )
                    for beacon2 in scanner2:
                        edges2 = sorted(
                            [
                                (distance(beacon2, x), x)
                                for x in scanner2
                                if beacon2 != x
                            ]
                        )
                        d1 = set(x[0] for x in edges1)
                        d2 = set(x[0] for x in edges2)
                        common_d = d1 & d2
                        if (
                            len(common_d) < 11
                        ):  # subtract one for the root point with distance 0 in both sets
                            continue

                        if i in scanner_locations and j not in scanner_locations:
                            (
                                scanner1_location,
                                scanner1_orientation,
                            ) = scanner_locations[i]
                            print(f"Beacons for {i} and {j}:")
                            scanner2_orientation = orient(
                                apply_orientation(beacon1, scanner1_orientation),
                                apply_orientation(edges1[0][1], scanner1_orientation),
                                beacon2,
                                edges2[0][1],
                            )

                            beacon1_location = plus(
                                scanner1_location,
                                apply_orientation(beacon1, scanner1_orientation),
                            )
                            print("Beacon location", beacon1_location, scanner1_orientation, scanner2_orientation)
                            scanner2_location = minus(
                                beacon1_location,
                                apply_orientation(beacon2, scanner2_orientation),
                            )
                            scanner_locations[j] = (
                                scanner2_location,
                                scanner2_orientation,
                            )
                            print(f"Scanner {j} at location:", scanner2_location)

    seen_beacons = set()
    for (i, (scanner_location, scanner_orientation)) in scanner_locations.items():
        beacons = [plus(scanner_location, apply_orientation(p, scanner_orientation)) for p in input[i]]
        seen_beacons.update(beacons)

    print("scanner locations:", scanner_locations)
    print("unique beacons:", len(seen_beacons))
    max_distance = max(distance(p1[0], p2[0]) for p1 in scanner_locations.values() for p2 in scanner_locations.values())
    print("max manhattan distance:", max_distance)


def parse_input(input: str) -> Input:
    sections = input.strip().split("\n\n")
    result = []
    for section in sections:
        result2 = []
        for line in section.splitlines()[1:]:
            (x, y, z) = line.split(",")
            result2.append((int(x), int(y), int(z)))
        result.append(result2)
    return result


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

     problem(test_input)
     problem(input)


if __name__ == "__main__":
    main()
