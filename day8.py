# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_signals_from_str(l, sep=" | "):
    left, mid, right = l.strip().partition(sep)
    assert mid == sep
    return (left.split(), right.split())


def get_signals_from_file(file_path="day8_input.txt"):
    with open(file_path) as f:
        return [get_signals_from_str(l) for l in f]


segments = [
    # A, B, C, D, E, F, G
    (1, 1, 1, 0, 1, 1, 1),
    (0, 0, 1, 0, 0, 1, 0),
    (1, 0, 1, 1, 1, 0, 1),
    (1, 0, 1, 1, 0, 1, 1),
    (0, 1, 1, 1, 0, 1, 0),
    (1, 1, 0, 1, 0, 1, 1),
    (1, 1, 0, 1, 1, 1, 1),
    (1, 0, 1, 0, 0, 1, 0),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 0, 1, 1),
]


def print_segments():
    """Ensure that the segment segments values are correct."""
    h = {0: "  ", 1: "--"}
    v = {0: " ", 1: "|"}
    for a, b, c, d, e, f, g in segments:
        print(" %s" % (h[a]))
        print("%s %s" % (v[b], v[c]))
        print(" %s" % (h[d]))
        print("%s %s" % (v[e], v[f]))
        print(" %s" % (h[g]))
        print()


def run_tests():
    signals = 42


def get_solutions():
    print_segments()
    signals = get_signals_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
