# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_bingo_from_file(file_path="day4_input.txt"):
    with open(file_path) as f:
        lines = [l.strip() for l in f]
        numbers = [int(n) for n in lines[0].split(",")]
        grids = []
        grid = []
        for line in lines[1:]:
            if line:
                grid.append([int(n) for n in line.split()])
                grids.append(grid)
            else:
                grid = []
        return numbers, grids

def get_score(grid, numbers_seen, last_number):
    return sum(n for line in grid for n in line if n not in numbers_seen) * last_number


def play_bingo(bingo):
    numbers, grids = bingo
    numbers_seen = set()
    for number in numbers:
        numbers_seen.add(number)
        for grid in grids:
            for i, line in enumerate(grid):
                if all(n in numbers_seen for n in line):
                    return get_score(grid, numbers_seen, number)
            for j in range(len(grid[0])):
                if all(line[j] in numbers_seen for line in grid):
                    return get_score(grid, numbers_seen, number)


def run_tests():
    bingo = get_bingo_from_file("day4_example_input.txt")
    assert play_bingo(bingo) == 4512


def get_solutions():
    bingo = get_bingo_from_file()
    print(play_bingo(bingo))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
