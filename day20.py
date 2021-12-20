# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime

VALUES = [".", "#"]


def get_algo_from_str(s):
    assert len(s) == 512 == 2 ** 9
    assert all(c in VALUES for c in s)
    assert s[0] != "#"
    return [c == "#" for c in s]


def get_points_from_lines(lines):
    points = set()
    for x, line in enumerate(lines):
        for y, val in enumerate(line):
            assert val in VALUES
            if val == "#":
                points.add((x, y))
    return points


def get_info_from_lines(lines):
    assert lines[1] == ""
    return get_algo_from_str(lines[0]), get_points_from_lines(lines[2:])


def get_info_from_file(file_path="day20_input.txt"):
    with open(file_path) as f:
        return get_info_from_lines([l.strip() for l in f])


def show_points(points):
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    x_range = list(range(min(x_vals), 1 + max(x_vals)))
    y_range = list(range(min(y_vals), 1 + max(y_vals)))
    for x in x_range:
        print("".join(VALUES[(x, y) in points] for y in y_range))
    print()


def get_square(point):
    x, y = point
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            yield x + dx, y + dy


def enhance(points, algo):
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    x_range = list(range(min(x_vals) - 2, 1 + 2 + max(x_vals)))
    y_range = list(range(min(y_vals) - 2, 1 + 2 + max(y_vals)))
    points2 = set()
    for x in x_range:
        for y in y_range:
            point = (x, y)
            square = int(
                "".join([str(int(p in points)) for p in get_square(point)]), base=2
            )
            algo_val = algo[square]
            if algo_val:
                points2.add(point)
    return points2


def enhance_n(points, algo, n):
    for _ in range(n):
        points = enhance(points, algo)
    return points


def run_tests():
    algo_str = "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
    algo = get_algo_from_str(algo_str)
    grid_str = [
        "#..#.",
        "#....",
        "##..#",
        "..#..",
        "..###",
    ]
    points = get_points_from_lines(grid_str)
    points = enhance_n(points, algo, 2)
    assert len(points) == 35


def get_solutions():
    pass
    # algo, points = get_info_from_file()
    # points = enhance_n(points, algo, 2)
    # print(len(points))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
