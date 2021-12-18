# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import ast


def is_pair(pair):
    return isinstance(pair, list)


def get_python_pair_from_str(s):
    for c in s:
        assert c in "[]1234567890,"
    return ast.literal_eval(s)


def get_pair_from_str(s):
    # /!\ This representation is slightly ambiguous and cannot make a difference between:
    # [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
    # [[3,[2,[1,[7,3]]],6,[5,[4,[3,2]]]]]
    # Maybe using the fact that we are representing *pairs* and not random list could help
    depth = 0
    digits = []
    pair = []
    for c in s:
        if c.isdigit():
            digits.append(c)
        else:
            if digits:
                pair.append([int("".join(digits)), depth])
            digits = []
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
            else:
                assert c == ","
    assert depth == 0
    assert digits == []
    return pair


def get_str_from_pair(pair):
    ret = []
    last_depth = 0
    first = True
    for n, depth in pair:
        if depth > last_depth:
            if not first:
                ret.append(",")
            ret.append("[" * (depth - last_depth))
        elif depth < last_depth:
            ret.append("]" * (last_depth - depth))
            if not first:
                ret.append(",")
        else:
            ret.append(",")
        ret.append(str(n))
        last_depth = depth
        first = False
    ret.append("]" * last_depth)
    return "".join(ret)


def get_pairs_from_file(file_path="day18_input.txt"):
    with open(file_path) as f:
        return [get_pair_from_str(l.strip()) for l in f]


def explode(pair):
    for i, (n, d) in enumerate(pair):
        if d >= 5:
            assert d == 5
            assert 0 <= i + 1 < len(pair)
            (n2, d2) = pair[i + 1]
            assert d2 == 5
            if 0 <= i - 1 < len(pair):
                pair[i - 1][0] += n
            if 0 <= i + 2 < len(pair):
                pair[i + 2][0] += n2
            pair[i + 1] = [0, d2 - 1]
            pair.pop(i)
            return True
    return False


def split(pair):
    for i, (n, d) in enumerate(pair):
        if n >= 10:
            half, rem = divmod(n, 2)
            left, right = half, half + rem
            pair.pop(i)
            pair.insert(i, [right, d + 1])
            pair.insert(i, [left, d + 1])
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
    pair = []
    for p in [pair1, pair2]:
        for n, d in p:
            pair.append([n, d + 1])
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
    pass
    # here we are stuck because of our representation of data


def string_handling_tests():
    tests = [
        "[[[[[9,8],1],2],3],4]",
        "[7,[6,[5,[4,[3,2]]]]]",
        "[[6,[5,[4,[3,2]]]],1]",
    ]
    for s in tests:
        pair = get_pair_from_str(s)
        s2 = get_str_from_pair(pair)
        assert s == s2
    # These cases do not lead to same string
    tests = [
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
    ]
    for s in tests:
        pair = get_pair_from_str(s)
        s2 = get_str_from_pair(pair)
        pair2 = get_pair_from_str(s2)
        assert pair == pair2


def explode_tests():
    tests = [
        "[[[[[9,8],1],2],3],4]",
        "[7,[6,[5,[4,[3,2]]]]]",
        "[[6,[5,[4,[3,2]]]],1]",
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
    ]
    for s in tests:
        pair = get_pair_from_str(s)
        assert explode(pair)
        # print(get_str_from_pair(pair))


def split_tests():
    tests = [
        "[[[[0,7],4],[15,[0,13]]],[1,1]]",
    ]
    for s in tests:
        pair = get_pair_from_str(s)
        assert split(pair)
        print(get_str_from_pair(pair))
        assert split(pair)
        print(get_str_from_pair(pair))


def reduce_tests():
    s = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
    pair = get_pair_from_str(s)
    reduce_pair(pair)
    print(get_str_from_pair(pair))


def add_tests():
    p1 = get_pair_from_str("[[[[4,3],4],4],[7,[[8,4],9]]]")
    p2 = get_pair_from_str("[1,1]")
    pair = add_pair(p1, p2)
    print(get_str_from_pair(pair))


def adds_tests():
    lst = ["[1,1]", "[2,2]", "[3,3]", "[4,4]"]
    pairs = [get_pair_from_str(s) for s in lst]
    pair = add_pairs(pairs)
    print(get_str_from_pair(pair))


def magnitude_tests():
    tests = [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ]
    for s, m in tests:
        pair = get_pair_from_str(s)


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


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
