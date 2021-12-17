# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re

target_area_re = r"^target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)$"


def get_target_area_from_string(s):
    m = re.match(target_area_re, s)
    return m.group(1, 2, 3, 4)


def get_target_area_from_file(file_path="day17_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_target_area_from_string(l.strip())


def position(vx, vy, step):
    x, y = 0, 0
    for s in range(step):
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
    return x, y


def x_position_slow(vx, step):
    x = 0
    for s in range(step):
        x += vx
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
    return x


def y_position_slow(vy, step):
    y = 0
    for s in range(step):
        y += vy
        vy -= 1
    return y


# Analysis of the x position
#############################
#       step is [0,  1,    2,      3,          ..., n
# x-velocity is [vx, vx-1, vx-2,   vx-3,       ..., vx - n, ...,
#      until it reaches 0 then it stays 0
# x-position is [0,  vx,   2*vx-1, 3*vx-(1+2), ..., n*vx - sum(1..n-1)
#      until it reaches the speed is 0 then position does not change
#  n*vx - sum(1..n-1) = n*vx - n*(n-1)/2
#                     = n * (vx - (n-1)/2)
def x_position(vx, step):
    sign = -1 if vx < 0 else 1
    vx = abs(vx)
    step = min(step, vx)
    return sign * (step * vx - (step * (step - 1)) // 2)


def max_x(vx):
    # max is reached after abs(vx) steps
    x1 = x_position(vx, abs(vx))
    x2 = x_position(vx, abs(vx) + 1)
    x3 = x_position(vx, abs(vx) + 2)
    assert x1 == x2 == x3
    return x1


# Analysis of the y position
#############################
#       step is [0,  1,    2,      3,          ..., n
# y-velocity is [vy, vy-1, vy-2,   vy-3,       ..., vy - n, ...,
#      until it reaches 0 (at the top) then same in reverse
# y-position is [0,  vy,   2*vy-1, 3*vy-(1+2), ...,
#      until it reaches the top then same in reverse
#  n*vy - sum(1..n-1) = n*vy - n*(n-1)/2
#                     = n * (vy - (n-1)/2)
def y_position(vy, step):
    return step * vy - (step * (step - 1)) // 2


def max_y(vy):
    if vy < 0:
        return 0
    # Assuming we shoot upward, top is reached after vy steps
    y1 = y_position(vy, vy)
    y2 = y_position(vy, vy + 1)
    assert y1 == y2
    return y1


def test_position(step, vx, vy, expected_position=None):
    x, y = position(vx, vy, step)
    if expected_position is not None:
        assert (x, y) == expected_position
    assert x_position_slow(vx, step) == x
    assert x_position(vx, step) == x
    assert y_position_slow(vy, step) == y
    assert y_position(vy, step) == y


def position_tests():
    vx, vy = 7, 2
    tests = [
        (0, (0, 0)),
        (1, (7, 2)),
        (2, (13, 3)),
        (3, (18, 3)),
        (4, (22, 2)),
        (5, (25, 0)),
        (6, (27, -3)),
        (7, (28, -7)),
        (8, (28, -12)),
    ]
    for s, pos in tests:
        test_position(s, vx, vy, pos)
    assert max_x(vx) == 28
    assert max_y(vy) == 3

    vx, vy = 6, 3
    tests = [
        (0, (0, 0)),
        (1, (6, 3)),
        (2, (11, 5)),
        (3, (15, 6)),
        (4, (18, 6)),
        (5, (20, 5)),
        (6, (21, 3)),
        (7, (21, 0)),
        (8, (21, -4)),
        (9, (21, -9)),
    ]
    for s, pos in tests:
        test_position(s, vx, vy, pos)
    assert max_x(vx) == 21
    assert max_y(vy) == 6

    # Additional tests
    vx, vy = 15, 10
    for s in range(16):
        test_position(s, vx, vy)
    assert max_x(vx) == 120
    assert max_y(vy) == 55
    vx, vy = -15, -10
    for s in range(16):
        test_position(s, vx, vy)
    assert max_x(vx) == -120
    assert max_y(vy) == 0


def run_tests():
    position_tests()


def get_solutions():
    target_area = get_target_area_from_file()
    print(target_area)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
