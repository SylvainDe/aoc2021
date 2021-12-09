# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_line_from_str(s):
    return [int(d) for d in s.strip()]


def get_grid_from_file(file_path="day9_input.txt"):
    with open(file_path) as f:
        return [get_line_from_str(l) for l in f]


def points(grid):
    for x, line in enumerate(grid):
        for y, val in enumerate(line):
            yield x, y, val


def neighbours(grid, x, y):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x2, y2 = x + dx, y + dy
        if 0 <= x2 < len(grid):
            l = grid[x2]
            if 0 <= y2 < len(l):
                yield l[y2]


def part1(grid):
    return sum(
        val + 1
        for x, y, val in points(grid)
        if all(v > val for v in neighbours(grid, x, y))
    )


def run_tests():
    grid = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ]
    grid = [get_line_from_str(l) for l in grid]
    assert part1(grid) == 15


def get_solutions():
    grid = get_grid_from_file()
    print(part1(grid))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
