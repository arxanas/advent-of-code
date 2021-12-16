import sys
from collections import *
from functools import *
from typing import *
from dataclasses import dataclass

TEST_INPUT = """
A0016C880162017C3686B18A3D4780
"""

Input = str


HEX = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def expand_hex(hex: str) -> str:
    return "".join(HEX[c] for c in hex)


@dataclass
class LiteralValuePacket:
    version: int
    value: int


@dataclass
class OperatorPacket:
    version: int
    operator: int
    subpackets: List["Packet"]


Packet = Union[LiteralValuePacket, OperatorPacket]


def parse_packet(packet: str) -> Tuple[Packet, str]:
    version = int(packet[0:3], base=2)
    type_id = int(packet[3:6], base=2)

    if type_id == 4:
        subvalues = []
        for i in range(6, len(packet), 5):
            batch = packet[i : i + 5]
            is_last = batch[0] == "0"
            subvalue = batch[1:]
            subvalues.append(subvalue)
            if is_last:
                end_index = i + 5
                break
        else:
            raise ValueError(f"End packet not found among these: {subvalues}")

        rest = packet[end_index:]
        value = int("".join(subvalues), base=2)
        return (LiteralValuePacket(version=version, value=value), rest)

    else:
        length_type_id = packet[6]
        PAYLOAD_START = 7
        if length_type_id == "0":
            total_length_in_bits = int(
                packet[PAYLOAD_START : PAYLOAD_START + 15], base=2
            )
            read_length = 0
            rest = packet[PAYLOAD_START + 15 :]
            subpackets = []
            while read_length < total_length_in_bits:
                assert rest
                (subpacket, rest2) = parse_packet(rest)
                read_length += len(rest) - len(rest2)
                rest = rest2
                subpackets.append(subpacket)
            assert read_length == total_length_in_bits
            return (
                OperatorPacket(
                    version=version, operator=type_id, subpackets=subpackets
                ),
                rest,
            )

        elif length_type_id == "1":
            num_subpackets = int(packet[PAYLOAD_START : PAYLOAD_START + 11], base=2)
            rest = packet[PAYLOAD_START + 11 :]
            subpackets = []
            for i in range(num_subpackets):
                assert (
                    rest
                ), f"Could not read more subpackets after parsing these: {subpackets!r}"
                (subpacket, rest) = parse_packet(rest)
                subpackets.append(subpacket)
            return (
                OperatorPacket(
                    version=version, operator=type_id, subpackets=subpackets
                ),
                rest,
            )

        else:
            raise ValueError(f"Unknown length type ID: {length_type_id}")


def hex_to_packet(hex: str) -> Packet:
    hex = expand_hex(hex)
    (result, _rest) = parse_packet(hex)
    return result


def test_parse_packet() -> None:
    assert hex_to_packet("D2FE28") == LiteralValuePacket(version=6, value=2021)
    assert parse_packet("11010001010")[0] == LiteralValuePacket(version=6, value=10)
    assert hex_to_packet("38006F45291200") == OperatorPacket(
        version=1,
        operator=6,
        subpackets=[
            LiteralValuePacket(version=6, value=10),
            LiteralValuePacket(version=2, value=20),
        ],
    )
    assert hex_to_packet("EE00D40C823060") == OperatorPacket(
        version=7,
        operator=3,
        subpackets=[
            LiteralValuePacket(version=2, value=1),
            LiteralValuePacket(version=4, value=2),
            LiteralValuePacket(version=1, value=3),
        ],
    )
    assert hex_to_packet("8A004A801A8002F478") == OperatorPacket(
        version=4,
        operator=2,
        subpackets=[
            OperatorPacket(
                version=1,
                operator=2,
                subpackets=[
                    OperatorPacket(
                        version=5,
                        operator=2,
                        subpackets=[LiteralValuePacket(version=6, value=15)],
                    )
                ],
            )
        ],
    )


def part1(input: Input) -> str:
    packet = hex_to_packet(input)

    def sum_versions(packet: Packet) -> int:
        if isinstance(packet, LiteralValuePacket):
            return packet.version
        elif isinstance(packet, OperatorPacket):
            return packet.version + sum(sum_versions(p) for p in packet.subpackets)

    return str(sum_versions(packet))


def test_part1() -> None:
    assert part1("8A004A801A8002F478") == "16"
    assert part1("620080001611562C8802118E34") == "12"
    assert part1("C0015000016115A2E0802F182340") == "23"
    assert part1("A0016C880162017C3686B18A3D4780") == "31"


def part2(input: Input) -> str:
    def eval(packet: Packet) -> int:
        if isinstance(packet, LiteralValuePacket):
            return packet.value
        elif isinstance(packet, OperatorPacket):
            if packet.operator == 0:
                return sum(eval(p) for p in packet.subpackets)
            elif packet.operator == 1:
                result = 1
                for p in packet.subpackets:
                    result *= eval(p)
                return result
            elif packet.operator == 2:
                return min(eval(p) for p in packet.subpackets)
            elif packet.operator == 3:
                return max(eval(p) for p in packet.subpackets)
            elif packet.operator == 5:
                [p1, p2] = packet.subpackets
                return int(eval(p1) > eval(p2))
            elif packet.operator == 6:
                [p1, p2] = packet.subpackets
                return int(eval(p1) < eval(p2))
            elif packet.operator == 7:
                [p1, p2] = packet.subpackets
                return int(eval(p1) == eval(p2))
            else:
                raise ValueError(f"Bad packet operator: {packet.operator}")

    return str(eval(hex_to_packet(input)))


def test_part2() -> None:
    assert part2("C200B40A82") == "3"
    assert part2("04005AC33890") == "54"
    assert part2("880086C3E88112") == "7"
    assert part2("CE00C43D881120") == "9"
    assert part2("D8005AC2A8F0") == "1"
    assert part2("F600BC2D8F") == "0"
    assert part2("9C005AC2F8F0") == "0"
    assert part2("9C0141080250320F1802104A08") == "1"


def parse_input(input: str) -> Input:
    return input.strip()


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
