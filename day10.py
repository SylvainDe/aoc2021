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

score = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

def get_corrupted_score(s):
    stack = list()
    for char in s:
        c, nb = characters[char]
        if nb == 1:
            stack.append(c)
        else:
            last = stack.pop()
            if last != c:
                return score[c]
    return 0

def get_score(lines):
    return sum(get_corrupted_score(l) for l in lines)


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
    assert get_score(lines) == 26397


def get_solutions():
    lines = get_lines_from_file()
    print(get_score(lines))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
