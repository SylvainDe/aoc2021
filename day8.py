# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_signals_from_str(l, sep=" | "):
    left, mid, right = l.strip().partition(sep)
    assert mid == sep
    return (left.split(), right.split())


def get_signals_from_file(file_path="day8_input.txt"):
    with open(file_path) as f:
        return [get_signals_from_str(l) for l in f]


RAW_SEGMENTS = [
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
    for a, b, c, d, e, f, g in RAW_SEGMENTS:
        print(" %s" % (h[a]))
        print("%s %s" % (v[b], v[c]))
        print(" %s" % (h[d]))
        print("%s %s" % (v[e], v[f]))
        print(" %s" % (h[g]))
        print()

LETTERS = "ABCDEFG"

SEGMENTS = {
    "".join(letter for bit, letter in zip(s, LETTERS) if bit): i
    for i, s in enumerate(RAW_SEGMENTS)
}

def group_by_len(strs):
    lengths = dict()
    for s in strs:
        lengths.setdefault(len(s), []).append(s)
    return lengths

SEGMENTS_BY_LEN = group_by_len(SEGMENTS.keys())


def decode_signal_pattern(signal):
    mapping = {l: set(L for L in LETTERS) for l in LETTERS.lower()}
    lengths = group_by_len(signal)
    for i in sorted(lengths):
        sig_i, seg_i = lengths[i], SEGMENTS_BY_LEN[i]
        assert len(sig_i) == len(seg_i)
        if len(sig_i) == 1:
            sig, seg = sig_i[0], seg_i[0]
            for l in sig:
                mapping[l] = mapping[l].intersection(set(seg))
    change = True
    while change:
        print(mapping)
        change = False
        equivalent_map = dict()
        for l, letters in mapping.items():
            equivalent_map.setdefault(tuple(letters), []).append(l)
        for lletters, uletters in equivalent_map.items():
            # If for instance 3 letters map to 3 letters, these can't be anywhere else
            if len(lletters) == len(uletters):
                for l, letters in mapping.items():
                    if tuple(letters) != lletters:
                        for c in lletters:
                            if c in letters:
                                change = True
                                letters.remove(c)
    # At this stage something smarter is required to go further (backtracing for instance)


def decode_signal(signal):
    left, right = signal
    decode_signal_pattern(left)


def decode_signals(signals):
    for s in signals:
        decode_signal(s)

def run_tests():
    signals = [get_signals_from_str("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")]
    print(decode_signals(signals))


def get_solutions():
    signals = get_signals_from_file()
    # print(decode_signals(signals))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
