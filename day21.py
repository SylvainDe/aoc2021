# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools


def get_positions_from_file(file_path="day21_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def deterministic_dice(sides=100):
    while True:
        for i in range(sides):
            yield i + 1


def get_sum_rolls(dice, n):
    return sum(next(dice) for _ in range(n))


def game(positions):
    # Shift positions by 1 to go from [1, 10] to [0, 9]
    nb_player = len(positions)
    positions = [pos - 1 for pos in positions]
    scores = [0 for pos in positions]
    dice = deterministic_dice()
    for i in itertools.count():
        player = i % nb_player
        new_pos = (positions[player] + get_sum_rolls(dice, 3)) % 10
        new_score = scores[player] + new_pos + 1
        positions[player] = new_pos
        scores[player] = new_score
        if new_score >= 1000:
            break
    nb_rolls = 3 * (i + 1)
    return min(scores) * nb_rolls


def run_tests():
    assert game([4, 8]) == 739785


def get_solutions():
    print(game([9, 6]))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
