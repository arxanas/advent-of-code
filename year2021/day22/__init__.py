import sys
from functools import lru_cache
from typing import List, Tuple, cast

TEST_INPUT = """
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""

TEST_INPUT2 = """
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
"""


Cube = Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]
Input = List[Tuple[str, Cube]]


def parse_input(lines: str) -> Input:
    result: List[Tuple[str, Cube]] = []
    for line in lines.strip().splitlines():
        (directive, words) = line.split(" ")
        parts = [s[2:] for s in words.split(",")]
        [xr, yr, zr] = [tuple(int(i) for i in part.split("..")) for part in parts]
        assert directive in ["on", "off"]
        xr = cast(Tuple[int, int], xr)
        yr = cast(Tuple[int, int], yr)
        zr = cast(Tuple[int, int], zr)
        result.append((directive, (xr, yr, zr)))
    return result


def part1(input: Input) -> object:
    cubes_on = set()
    for (directive, (xr, yr, zr)) in input:
        for x in range(max(-50, xr[0]), min(50, xr[1]) + 1):
            for y in range(max(-50, yr[0]), min(50, yr[1]) + 1):
                for z in range(max(-50, zr[0]), min(50, zr[1]) + 1):
                    if directive == "on":
                        cubes_on.add((x, y, z))
                    else:
                        assert directive == "off"
                        cubes_on.discard((x, y, z))
    return len(cubes_on)


def clamp(a: int, b: int, c: int) -> int:
    if b <= a:
        return a
    elif b >= c:
        return c
    else:
        return b


@lru_cache(maxsize=None)
def cube_intersect(c1: Cube, c2: Cube) -> Cube:
    ((x11, x12), (y11, y12), (z11, z12)) = c1
    ((x21, x22), (y21, y22), (z21, z22)) = c2
    xr = (clamp(x11, x21, x12), clamp(x11, x22, x12))
    yr = (clamp(y11, y21, y12), clamp(y11, y22, y12))
    zr = (clamp(z11, z21, z12), clamp(z11, z22, z12))
    assert xr[0] <= xr[1]
    assert yr[0] <= yr[1]
    assert zr[0] <= zr[1]
    result = (xr, yr, zr)
    return result


def test_intersect_cubes() -> None:
    assert cube_intersect(((0, 5), (0, 10), (0, 15)), ((1, 4), (2, 11), (-1, 16))) == (
        (1, 4),
        (2, 10),
        (0, 15),
    )
    assert cube_intersect(
        ((-50, 50), (-50, 50), (-50, 50)),
        ((-54112, -39298), (-85059, -49293), (-27449, 7877)),
    ) == ((-50, -50), (-50, -50), (-50, 50))


def cube_size(cube: Cube) -> int:
    (xr, yr, zr) = cube

    def a(x):
        return int(abs(x))

    return a(xr[1] - xr[0]) * a(yr[1] - yr[0]) * a(zr[1] - zr[0])


def test_cube_union_size() -> None:
    cubes = (
        ((0, 1), (0, 1), (0, 2)),
        ((0, 1), (0, 1), (1, 3)),
        ((1, 2), (0, 1), (1, 3)),
    )
    assert cube_union_size(cubes) == 5


@lru_cache(maxsize=None)
def cube_union_size(cubes: Tuple[Cube]) -> int:
    """Exponential complexity -- too slow."""
    if len(cubes) == 0:
        return 0

    tl: List[Cube]
    [hd, *tl] = cubes
    size_hd = cube_size(hd)
    size_tl = cube_union_size(tuple(tl))
    tl_inter = [cube_intersect(hd, tl_cube) for tl_cube in tl]
    tl_inter = [x for x in tl_inter if x is not None]
    size_overlap = cube_union_size(tuple(tl_inter))
    return size_hd + size_tl - size_overlap


def cut_ranges(r11, r12, r21, r22):
    rs = []
    assert r11 <= r12
    assert r21 <= r22
    points = sorted([r11, r12, r21, r22])
    for (l, r) in zip(points, points[1:]):
        rs.append((l, r))
    return sorted(set((a, b) for (a, b) in rs if r11 <= a < b <= r12))


def cube_subtract(big_cube: Cube, small_cube: Cube) -> List[Cube]:
    ((xr11, xr12), (yr11, yr12), (zr11, zr12)) = big_cube
    ((xr21, xr22), (yr21, yr22), (zr21, zr22)) = small_cube

    sub_cube_to_remove = cube_intersect(big_cube, small_cube)
    if cube_size(sub_cube_to_remove) == 0:
        return [big_cube]

    xrs = cut_ranges(xr11, xr12, xr21, xr22)
    yrs = cut_ranges(yr11, yr12, yr21, yr22)
    zrs = cut_ranges(zr11, zr12, zr21, zr22)
    result = []
    for xr in xrs:
        for yr in yrs:
            for zr in zrs:
                if (xr, yr, zr) != sub_cube_to_remove:
                    result.append((xr, yr, zr))

    for result_cube in result:
        assert cube_intersect(big_cube, result_cube) == result_cube
        assert cube_size(cube_intersect(result_cube, small_cube)) == 0
    assert cube_size(big_cube) == sum(cube_size(c) for c in result) + cube_size(
        sub_cube_to_remove
    )
    assert (
        cube_size(big_cube)
        + cube_size(small_cube)
        - cube_size(cube_intersect(big_cube, small_cube))
    ) == sum(cube_size(c) for c in result) + cube_size(small_cube)

    return result


def test_subtract_cubes() -> None:
    assert (
        len(
            cube_subtract(
                ((0, 2), (0, 2), (0, 2)),
                ((0, 1), (0, 1), (0, 1)),
            )
        )
        == 7
    )
    assert (
        len(
            cube_subtract(
                ((0, 3), (0, 3), (0, 3)),
                ((1, 2), (1, 2), (1, 2)),
            )
        )
        == 26
    )
    assert (
        len(
            cube_subtract(
                ((0, 3), (0, 3), (0, 3)),
                ((1, 3), (0, 3), (0, 3)),
            )
        )
        == 1
    )
    assert (
        len(
            cube_subtract(
                ((0, 3), (0, 3), (0, 3)),
                ((1, 3), (1, 3), (0, 3)),
            )
        )
        == 3
    )
    assert sorted(
        cube_subtract(((1, 3), (0, 2), (0, 1)), ((0, 2), (0, 1), (0, 1)))
    ) == [
        ((1, 2), (1, 2), (0, 1)),
        ((2, 3), (0, 1), (0, 1)),
        ((2, 3), (1, 2), (0, 1)),
    ]
    cube_subtract(((1, 3), (0, 1), (0, 1)), ((0, 2), (0, 1), (1, 2)))
    cube_subtract(((0, 1), (0, 1), (0, 1)), ((0, 1), (0, 1), (2, 3)))
    cube_subtract(((0, 1), (1, 2), (0, 1)), ((0, 1), (0, 3), (0, 1)))


def part2(input: Input) -> object:
    cubes: List[Cube] = []
    for (directive, cube) in input:
        # Cube dimensions are inclusive on both sides, but our math is exclusive
        # on the right side of a given range.
        ((x1, x2), (y1, y2), (z1, z2)) = cube
        cube = ((x1, x2 + 1), (y1, y2 + 1), (z1, z2 + 1))

        if cube_size(cube) == 0:
            continue
        new_cubes = []
        for old_cube in cubes:
            new_cubes.extend(cube_subtract(old_cube, cube))
        if directive == "on":
            new_cubes.append(cube)
        cubes = [c for c in new_cubes if cube_size(c) > 0]

    return sum(cube_size(c) for c in cubes)


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)
    test_input2 = parse_input(TEST_INPUT2)

    restrict_cube = ((-50, 50), (-50, 50), (-50, 50))
    test_input_50 = [(d, cube_intersect(restrict_cube, c)) for (d, c) in test_input]

    print("test 1.1:", part1(test_input))
    print("test 1.2:", part2(test_input_50), "(should be same as test 1.1)")
    print("part 1:", part1(input))
    print("test 2:", part2(test_input2))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
