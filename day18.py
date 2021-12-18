# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools


def get_pair_from_str(s):
    digits = []
    pair = []
    for c in s:
        if c.isdigit():
            digits.append(c)
        else:
            if digits:
                pair.append(int("".join(digits)))
                digits = []
            pair.append(c)
    assert digits == []
    return pair


def get_str_from_pair(pair):
    return "".join(str(e) for e in pair)


def get_pairs_from_file(file_path="day18_input.txt"):
    with open(file_path) as f:
        return [get_pair_from_str(l.strip()) for l in f]


def explode(pair):
    nb_pos = []
    explo = None
    depth = 0
    for i, e in enumerate(pair):
        if e == "[":
            depth += 1
        elif e == "]":
            depth -= 1
        elif e == ",":
            pass
        else:
            assert isinstance(e, int)
            nb_pos.append(i)
            if depth >= 5:
                assert depth == 5
                if explo is None:
                    explo = len(nb_pos) - 1
    assert depth == 0
    if explo is not None:
        i = nb_pos[explo]
        assert 0 <= explo < len(nb_pos)
        assert 0 <= explo + 1 < len(nb_pos)
        assert nb_pos[explo + 1] == i + 2
        if 0 <= explo - 1 < len(nb_pos):
            pair[nb_pos[explo - 1]] += pair[i]
        if 0 <= explo + 2 < len(nb_pos):
            pair[nb_pos[explo + 2]] += pair[nb_pos[explo + 1]]
        pair.pop(i - 1)
        pair.pop(i - 1)
        pair.pop(i - 1)
        pair.pop(i - 1)
        pair[i - 1] = 0
        return True
    return False


def split(pair):
    for i, e in enumerate(pair):
        if isinstance(e, int) and e >= 10:
            half, rem = divmod(e, 2)
            left, right = half, half + rem
            pair.pop(i)
            for item in reversed(["[", left, ",", right, "]"]):
                pair.insert(i, item)
            return True
    return False


def reduce_pair(pair):
    while True:
        if explode(pair):
            continue
        if split(pair):
            continue
        break


def add_pair(pair1, pair2):
    pair = ["["] + pair1 + [","] + pair2 + ["]"]
    reduce_pair(pair)
    return pair


def add_pairs(lst):
    res = None
    for pair in lst:
        if res is None:
            res = pair
        else:
            res = add_pair(res, pair)
    return res


def magnitude(pair):
    if len(pair) == 1:
        assert isinstance(pair[0], int)
        return pair[0]
    depth = 0
    coma = None
    for i, e in enumerate(pair):
        if e == "[":
            depth += 1
        elif e == "]":
            depth -= 1
        elif isinstance(e, int):
            pass
        else:
            assert e == ","
            if depth == 1:
                assert coma is None
                coma = i
    assert depth == 0
    assert coma is not None
    left = pair[1:coma]
    right = pair[coma + 1 : -1]
    return 3 * magnitude(left) + 2 * magnitude(right)


def string_handling_tests():
    tests = [
        "[[[[[9,8],1],2],3],4]",
        "[7,[6,[5,[4,[3,2]]]]]",
        "[[6,[5,[4,[3,2]]]],1]",
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
        "[[9,1],[1,9]]",
    ]
    for s in tests:
        pair = get_pair_from_str(s)
        s2 = get_str_from_pair(pair)
        assert s == s2


def explode_tests():
    tests = [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ]
    for s1, s2 in tests:
        pair = get_pair_from_str(s1)
        assert explode(pair)
        assert get_str_from_pair(pair) == s2


def split_tests():
    tests = [
        ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
        ("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"),
    ]
    for s, s2 in tests:
        pair = get_pair_from_str(s)
        assert split(pair)
        assert get_str_from_pair(pair) == s2


def reduce_tests():
    s = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
    s2 = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    pair = get_pair_from_str(s)
    reduce_pair(pair)
    assert get_str_from_pair(pair) == s2


def add_tests():
    p1 = get_pair_from_str("[[[[4,3],4],4],[7,[[8,4],9]]]")
    p2 = get_pair_from_str("[1,1]")
    pair = add_pair(p1, p2)
    s = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    assert get_str_from_pair(pair) == s


def adds_tests():
    lst = ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"]
    pairs = [get_pair_from_str(s) for s in lst]
    pair = add_pairs(pairs)
    assert get_str_from_pair(pair) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"


def magnitude_tests():
    tests = [
        ("[9,1]", 29),
        ("[1,9]", 21),
        ("[[9,1],[1,9]]", 129),
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ]
    for s, m in tests:
        pair = get_pair_from_str(s)
        assert magnitude(pair) == m


def run_tests():
    string_handling_tests()
    explode_tests()
    split_tests()
    reduce_tests()
    add_tests()
    adds_tests()
    magnitude_tests()


def get_solutions():
    pairs = get_pairs_from_file()
    pair = add_pairs(pairs)
    print(magnitude(pair))
    print(max(magnitude(add_pair(a, b)) for a, b in itertools.permutations(pairs, 2)))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
