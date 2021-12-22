# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools

actions = {
    "on": True,
    "off": False,
}


def get_range(s):
    name, middle, values = s.partition("=")
    assert middle == "="
    return tuple(int(val) for val in values.split(".."))


def get_instruction_from_string(s):
    action, middle, ranges = s.partition(" ")
    assert middle == " "
    return actions[action], [get_range(v) for v in ranges.split(",")]


def get_instructions_from_strings(lines):
    return [get_instruction_from_string(l.strip()) for l in lines]


def get_instructions_from_file(file_path="day22_input.txt"):
    with open(file_path) as f:
        return get_instructions_from_strings(f)


def range_intersection(interval1, interval2):
    beg1, end1 = interval1
    beg2, end2 = interval2
    assert beg1 <= end1
    assert beg2 <= end2
    beg3 = max(beg1, beg2)
    end3 = min(end1, end2)
    if beg3 <= end3:
        return range(beg3, end3 + 1)
    return []


def follow_instruction(instruction, points, interval):
    action, ranges = instruction
    ranges = [range_intersection(interval, r) for r in ranges]
    points_changed = set(itertools.product(*ranges))
    if action:
        return points | points_changed
    else:
        return points - points_changed


def follow_instructions(instructions, interval):
    points = set()
    for instruction in instructions:
        points = follow_instruction(instruction, points, interval)
    return points


def run_tests():
    interval = (-50, 50)
    instructions = [get_instruction_from_string("on x=10..12,y=10..12,z=10..12")]
    assert len(follow_instructions(instructions, interval)) == 27

    instructions = [
        "on x=10..12,y=10..12,z=10..12",
        "on x=11..13,y=11..13,z=11..13",
        "off x=9..11,y=9..11,z=9..11",
        "on x=10..10,y=10..10,z=10..10",
    ]
    instructions = get_instructions_from_strings(instructions)
    assert len(follow_instructions(instructions, interval)) == 39

    instructions = [
        "on x=-20..26,y=-36..17,z=-47..7",
        "on x=-20..33,y=-21..23,z=-26..28",
        "on x=-22..28,y=-29..23,z=-38..16",
        "on x=-46..7,y=-6..46,z=-50..-1",
        "on x=-49..1,y=-3..46,z=-24..28",
        "on x=2..47,y=-22..22,z=-23..27",
        "on x=-27..23,y=-28..26,z=-21..29",
        "on x=-39..5,y=-6..47,z=-3..44",
        "on x=-30..21,y=-8..43,z=-13..34",
        "on x=-22..26,y=-27..20,z=-29..19",
        "off x=-48..-32,y=26..41,z=-47..-37",
        "on x=-12..35,y=6..50,z=-50..-2",
        "off x=-48..-32,y=-32..-16,z=-15..-5",
        "on x=-18..26,y=-33..15,z=-7..46",
        "off x=-40..-22,y=-38..-28,z=23..41",
        "on x=-16..35,y=-41..10,z=-47..6",
        "off x=-32..-23,y=11..30,z=-14..3",
        "on x=-49..-5,y=-3..45,z=-29..18",
        "off x=18..30,y=-20..-8,z=-3..13",
        "on x=-41..9,y=-7..43,z=-33..15",
        "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877",
        "on x=967..23432,y=45373..81175,z=27513..53682",
    ]
    instructions = get_instructions_from_strings(instructions)
    assert len(follow_instructions(instructions, interval)) == 590784


def get_solutions():
    interval = (-50, 50)
    instructions = get_instructions_from_file()
    print(len(follow_instructions(instructions, interval)))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
