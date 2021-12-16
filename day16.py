# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections
import functools
import operator


def get_str_from_file(file_path="day16_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


hex_table = {s: bin(int(s, 16))[2:].zfill(4) for s in "0123456789ABCDEF"}

Packet = collections.namedtuple("Packet", ["version", "type_id", "content"])


def get_bits_from_str(s):
    return "".join(hex_table[h] for h in s)


def bits_to_int(bits):
    return int("".join(bits), base=2)


def next_n(it, n):
    for i in range(n):
        yield next(it)


def next_n_bits_to_int(bit_iter, n):
    return bits_to_int(next_n(bit_iter, n))


def parse_literal_value_packet(bit_iter):
    content = []
    while True:
        prefix = next(bit_iter)
        content.extend(next_n(bit_iter, 4))
        if prefix == "0":
            break
    return bits_to_int(content)


def parse_operator_packet(bit_iter):
    length_type = next(bit_iter)
    if length_type == "0":
        total_length = next_n_bits_to_int(bit_iter, 15)
        sub_packets = "".join(next_n(bit_iter, total_length))
        sub_packets_iter = iter(sub_packets)
        packets = []
        try:
            while True:
                packets.append(parse_packet(sub_packets_iter))
        except RuntimeError:
            return packets
    else:
        nb_packets = next_n_bits_to_int(bit_iter, 11)
        packets = [parse_packet(bit_iter) for i in range(nb_packets)]
        return packets


def parse_packet(bits):
    bit_iter = iter(bits)
    version = next_n_bits_to_int(bit_iter, 3)
    packet_type = next_n_bits_to_int(bit_iter, 3)
    content = (
        parse_literal_value_packet(bit_iter)
        if packet_type == 4
        else parse_operator_packet(bit_iter)
    )
    return Packet(version, packet_type, content)


def sum_version_numbers(packet):
    return packet.version + (
        0
        if packet.type_id == 4
        else sum(sum_version_numbers(p) for p in packet.content)
    )


def mult(iterable, start=1):
    """Returns the product of an iterable - like the sum builtin."""
    return functools.reduce(operator.mul, iterable, start)


def eval_packet(packet):
    type_id = packet.type_id
    content = packet.content
    if type_id == 0:
        return sum(eval_packet(p) for p in content)
    elif type_id == 1:
        return mult(eval_packet(p) for p in content)
    elif type_id == 2:
        return min(eval_packet(p) for p in content)
    elif type_id == 3:
        return max(eval_packet(p) for p in content)
    elif type_id == 4:
        return content
    elif type_id == 5:
        return int(eval_packet(content[0]) > eval_packet(content[1]))
    elif type_id == 6:
        return int(eval_packet(content[0]) < eval_packet(content[1]))
    elif type_id == 7:
        return int(eval_packet(content[0]) == eval_packet(content[1]))
    else:
        assert False


def run_tests():
    s = "D2FE28"
    b = get_bits_from_str(s)
    assert b == "110100101111111000101000"
    p = parse_packet(b)
    assert p == Packet(version=6, type_id=4, content=2021)

    s = "38006F45291200"
    b = get_bits_from_str(s)
    assert b == "00111000000000000110111101000101001010010001001000000000"
    p = parse_packet(b)
    assert p == Packet(
        version=1,
        type_id=6,
        content=[
            Packet(version=6, type_id=4, content=10),
            Packet(version=2, type_id=4, content=20),
        ],
    )

    s = "EE00D40C823060"
    b = get_bits_from_str(s)
    assert b == "11101110000000001101010000001100100000100011000001100000"
    p = parse_packet(b)
    assert p == Packet(
        version=7,
        type_id=3,
        content=[
            Packet(version=2, type_id=4, content=1),
            Packet(version=4, type_id=4, content=2),
            Packet(version=1, type_id=4, content=3),
        ],
    )

    examples = [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ]
    for s, v in examples:
        assert sum_version_numbers(parse_packet(get_bits_from_str(s))) == v

    examples = [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ]
    for s, v in examples:
        assert eval_packet(parse_packet(get_bits_from_str(s))) == v


def get_solutions():
    s = get_str_from_file()
    p = parse_packet(get_bits_from_str(s))
    print(sum_version_numbers(p))
    print(eval_packet(p))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
