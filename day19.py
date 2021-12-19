# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import itertools
import collections

scanner_re = r"^--- scanner (\d+) ---$"


def get_info_from_lines(lines):
    scanner = None
    info = []
    scanner_info = []
    for l in lines:
        if scanner is None:
            m = re.match(scanner_re, l)
            scanner = int(m.group(1))
            assert scanner == len(info)
        elif l == "":
            info.append(scanner_info)
            scanner = None
            scanner_info = []
        else:
            pos = [int(v) for v in l.split(",")]
            scanner_info.append(pos)
    assert scanner_info
    info.append(scanner_info)
    return info


def get_info_from_file(file_path="day19_input.txt"):
    with open(file_path) as f:
        return get_info_from_lines([l.strip() for l in f])


def gap(p1, p2):
    # Compute some tuple representing the gap between 2 points
    # That value does not depend on the position/orientation of the observer
    return tuple(sorted(abs(c1 - c2) for c1, c2 in zip(p1, p2)))


def get_gaps(info):
    # Mapping gaps to list of (scanner number, beacon1, beacon2)
    gaps = dict()
    for i, scanner_info in enumerate(info):
        for (b1, p1), (b2, p2) in itertools.combinations(enumerate(scanner_info), 2):
            gaps.setdefault(gap(p1, p2), []).append((i, b1, b2))
    return gaps


def get_overlaps(info, nb_common=12):
    gaps = get_gaps(info)
    # If scanners have n overlapping points, we expect n*(n-1)/2
    # common pairs of points seen from the 2 scanners
    nb_overlaps = nb_common * (nb_common - 1) // 2
    # Count similar gaps for each pair of scanners
    overlaps = collections.Counter()
    for gap, points in gaps.items():
        for p1, p2 in itertools.combinations(points, 2):
            i, _, _ = p1
            j, _, _ = p2
            k = tuple(sorted([i, j]))
            overlaps[k] += 1
    return [pair for pair, count in overlaps.items() if count >= nb_overlaps]


def run_tests():
    info = get_info_from_file("day19_example_input.txt")
    overlaps = get_overlaps(info)
    assert (0, 1) in overlaps
    assert (1, 4) in overlaps


def get_solutions():
    info = get_info_from_file()
    # print(get_overlaps(info))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
