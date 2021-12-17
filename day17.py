# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import math

target_area_re = r"^target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)$"


def get_target_area_from_string(s):
    m = re.match(target_area_re, s)
    return [int(v) for v in m.group(1, 2, 3, 4)]


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


# Finding whether a point or an area is reachable
def yield_divisors_using_divisions(n):
    """Yields distinct divisors of n.

    This uses sucessive divisions so it can be slower than
    yield_divisors_using_primes_factorisation on big inputs but it is easier
    to understand, the upper bound of O(sqrt(n)) is guarantee and faster on
    small inputs."""
    assert n > 0
    yield 1
    if n > 1:
        yield n
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                j = n // i
                yield i
                if i != j:
                    yield j


def velocities_to_reach(x, y):
    sign = -1 if x < 0 else 1
    x = abs(x)
    # if step <= vx: x = step * vx - (step * (step - 1)) / 2     (1)
    # otherwise:     x = vx*vx - (vx * (vx - 1)) / 2             (2)
    # in all cases:  y = step * vy - (step * (step - 1)) / 2
    #
    # Assuming case (1):
    #  x - y = step * (vx - vy)
    d = abs(x - y)
    # If x == y, either
    #  - step == 0 (uninteresting)
    #  - vx == vy
    if d == 0:
        # print(x, y, "is reachable at various speeds")
        # assert False  # TODO: Do properly
        return
    # If x != y: step divides x - y
    divs = list(yield_divisors_using_divisions(d))
    for step in divs:
        val = step * (1 - step) // 2
        vx, remx = divmod(x - val, step)
        vy, remy = divmod(y - val, step)
        if remx == remy == 0:
            assert abs(vx - vy) * step == d
            if step <= vx:
                assert position(vx, vy, step) == (x, y)
                yield sign * vx, vy
    # Assuming case (2)
    # v² + v - 2x == 0
    # /\ = 1 + 8x
    delta = 1 + 8 * x
    delta_root = int(math.sqrt(delta))
    vx_values = set()
    if delta_root * delta_root == delta:
        for val in [(-1 - delta_root), (-1 + delta_root)]:
            vx, rem = divmod(val, 2)
            if rem == 0 and vx >= 0:
                assert x_position(vx, vx + 1) == x
                vx_values.add(vx)
    for vx in vx_values:
        # vy = (2*y) + s*(s-1) / (2*s)
        for step in range(vx, vx + 2000):  # TODO: Improve range
            val = 2 * y + step * (step - 1)
            vy, remy = divmod(val, 2 * step)
            if remy == 0:
                assert position(vx, vy, step) == (x, y)
                yield sign * vx, vy


def find_velocities(area):
    mini_x, maxi_x, mini_y, maxi_y = area
    velocities = set()
    for x in range(mini_x, maxi_x + 1):
        for y in range(mini_y, maxi_y):
            for v in velocities_to_reach(x, y):
                velocities.add(v)
    return velocities


def select_highest(velocities):
    vys = {vy for vx, vy in velocities}
    heights = [max_y(vy) for vy in vys]
    return max(heights)


def test_position(step, vx, vy, expected_position=None):
    x, y = position(vx, vy, step)
    if expected_position is not None:
        assert (x, y) == expected_position
    assert x_position_slow(vx, step) == x
    assert x_position(vx, step) == x
    assert y_position_slow(vy, step) == y
    assert y_position(vy, step) == y
    if (x, y) != (0, 0):
        if 0 <= step <= vx:
            assert x - y == (vx - vy) * step
        elif 0 <= vx <= step:
            assert 2 * x == vx * (vx + 1)
        velocities = list(velocities_to_reach(x, y))
        assert (vx, vy) in velocities


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

    vx, vy = 9, 0
    tests = [
        (0, (0, 0)),
        (1, (9, 0)),
        (2, (17, -1)),
        (3, (24, -3)),
        (4, (30, -6)),
        (5, (35, -10)),
        (6, (39, -15)),
        (7, (42, -21)),
        (8, (44, -28)),
        (9, (45, -36)),
    ]
    for s, pos in tests:
        test_position(s, vx, vy, pos)
    assert max_x(vx) == 45
    assert max_y(vy) == 0

    vx, vy = 17, -4
    tests = [
        (0, (0, 0)),
        (1, (17, -4)),
        (2, (33, -9)),
        (3, (48, -15)),
        (4, (62, -22)),
        (5, (75, -30)),
        (6, (87, -39)),
        (7, (98, -49)),
        (8, (108, -60)),
        (9, (117, -72)),
    ]
    for s, pos in tests:
        test_position(s, vx, vy, pos)

    vx, vy = 6, 9
    tests = [
        (0, (0, 0)),
        (1, (6, 9)),
        (2, (11, 17)),
        (3, (15, 24)),
        (4, (18, 30)),
        (5, (20, 35)),
        (6, (21, 39)),
        (7, (21, 42)),
        (8, (21, 44)),
        (9, (21, 45)),
    ]
    for s, pos in tests:
        test_position(s, vx, vy, pos)

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
    vx, vy = 15, -10
    for s in range(16):
        test_position(s, vx, vy)
    assert max_x(vx) == 120
    assert max_y(vy) == 0
    vx, vy = -15, 10
    for s in range(16):
        test_position(s, vx, vy)
    assert max_x(vx) == -120
    assert max_y(vy) == 55


def range_tests():
    target_area = (20, 30, -10, -5)
    assert select_highest(find_velocities(target_area)) == 45


def run_tests():
    position_tests()
    range_tests()


def get_solutions():
    target_area = get_target_area_from_file()
    print(select_highest(find_velocities(target_area)))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
