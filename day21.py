# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools


def get_position_from_line(s):
    return int(s.split(": ")[-1])


def get_positions_from_file(file_path="day21_input.txt"):
    with open(file_path) as f:
        return [get_position_from_line(l.strip()) for l in f]


def deterministic_dice(sides=100):
    while True:
        for i in range(sides):
            yield i + 1


def get_sum_rolls(dice, n):
    return sum(next(dice) for _ in range(n))


def game(positions, final_score=1000, rolls=3):
    nb_player = len(positions)
    # Shift positions by 1 to go from [1, 10] to [0, 9]
    players = [(pos - 1, 0) for pos in positions]
    dice = deterministic_dice()
    for i in itertools.count():
        player = i % nb_player
        pos, score = players[player]
        pos += get_sum_rolls(dice, rolls)
        pos %= 10
        score += pos + 1  # Shift position back to compute score
        players[player] = (pos, score)
        if score >= final_score:
            nb_rolls = rolls * (i + 1)
            return min([s for p, s in players]) * nb_rolls


def run_tests():
    positions = [4, 8]
    assert game(positions) == 739785


def get_solutions():
    positions = get_positions_from_file()
    print(game(positions))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
