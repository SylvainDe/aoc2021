# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


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
                yield x2, y2, l[y2]


def get_low_points(grid):
    return (
        (x, y, val)
        for x, y, val in points(grid)
        if all(v > val for _, _, v in neighbours(grid, x, y))
    )


def print_point_sets(grid, points):
    for x, line in enumerate(grid):
        print("".join("X" if (x, y) in points else " " for y, val in enumerate(line)))


def part1(grid):
    return sum(val + 1 for x, y, val in get_low_points(grid))


def low_points_from(grid, x, y):
    low_points = set()
    queue = collections.deque([(x, y)])
    while queue:
        x, y = queue.popleft()
        val = grid[x][y]
        lower_points = [(x2, y2) for x2, y2, v in neighbours(grid, x, y) if v < val]
        if len(lower_points) == 0:
            low_points.add((x, y))
        else:
            for x2, y2 in lower_points:
                queue.append((x2, y2))
    return low_points


def part2(grid):
    basins = dict()
    for x, y, val in points(grid):
        if val != 9:
            low_points = low_points_from(grid, x, y)
            if len(low_points) == 1:
                low_point = low_points.pop()
                basins.setdefault(low_point, []).append((x, y))
    basins_len = sorted([len(basin) for basin in basins.values()], reverse=True)
    return basins_len[0] * basins_len[1] * basins_len[2]


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
    assert part2(grid) == 1134


def get_solutions():
    grid = get_grid_from_file()
    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
