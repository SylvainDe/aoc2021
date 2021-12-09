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


def part2(grid):
    flows = dict()
    for x, y, val in points(grid):
        lower_points = [(x2, y2) for x2, y2, v in neighbours(grid, x, y) if v < val]
        # This is a miserunderstanding of the statement "flow to a single point": we should consider the final points
        if len(lower_points) == 1:
            x2, y2 = lower_points[0]
            flows.setdefault((x2, y2), []).append((x, y))
    print(flows)

    basins = []
    for x, y, _ in get_low_points(grid):
        queue = collections.deque([(x, y)])
        seen = set()
        while queue:
            p = queue.popleft()
            if p not in seen:
                seen.add(p)
                for p2 in flows.get(p, []):
                    queue.append(p2)
        basins.append(len(seen))
        print("basin found")
        print_point_sets(grid, seen)
    print(sorted(basins))


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
    print(part2(grid))


def get_solutions():
    grid = get_grid_from_file()
    print(part1(grid))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
