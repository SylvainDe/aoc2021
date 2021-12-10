# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_lines_from_file(file_path="day10_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


pairs = ["()", "{}", "<>", "[]"]

characters = dict()
for (a, b) in pairs:
    characters[a] = (b, 1)
    characters[b] = (b, -1)

corruption_score = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def parse_string(s):
    """Return (first invalid char (or None), expected stack (or empty)."""
    stack = list()
    for char in s:
        c, nb = characters[char]
        if nb == 1:
            stack.append(c)
        elif stack and stack[-1] == c:
            stack.pop()
        else:
            return c, []
    return None, stack


def get_corruption_score(s):
    invalid, _ = parse_string(s)
    return corruption_score.get(invalid, 0)


completion_score = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def get_completion_score(s):
    _, stack = parse_string(s)
    return sum(completion_score[c] * 5 ** i for i, c in enumerate(stack))


def get_corruption_final_score(lines):
    return sum(get_corruption_score(l) for l in lines)


def get_completion_final_score(lines):
    scores = [get_completion_score(l) for l in lines]
    scores = sorted([s for s in scores if s])
    return scores[len(scores) // 2]


def run_tests():
    lines = [
        "[({(<(())[]>[[{[]{<()<>>",
        "[(()[<>])]({[<{<<[]>>(",
        "{([(<{}[<>[]}>{[]{[(<()>",
        "(((({<>}<{<{<>}{[]{[]{}",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "{<[[]]>}<{[{[{[]{()[[[]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
        "<{([{{}}[<[[[<>{}]]]>[]]",
    ]
    assert get_corruption_final_score(lines) == 26397
    assert get_completion_score("[({(<(())[]>[[{[]{<()<>>") == 288957
    assert get_completion_score("<{([{{}}[<[[[<>{}]]]>[]]") == 294
    assert get_completion_final_score(lines) == 288957
    assert parse_string(")") == (")", [])


def get_solutions():
    lines = get_lines_from_file()
    print(get_corruption_final_score(lines))
    print(get_completion_final_score(lines))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
