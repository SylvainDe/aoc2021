# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math


def get_crabs_from_file(file_path="day7_input.txt"):
    with open(file_path) as f:
        for l in f:
            return [int(v) for v in l.strip().split(",")]


def get_best_position(crabs):
    crabs = sorted(crabs)
    n = len(crabs)
    # Get media position
    costs = []
    for cand in [(n-1)//2, n//2, (n+1)//2]:
        pos = crabs[cand]
        cost = sum(abs(crab-pos) for crab in crabs)
        costs.append(cost)
    return min(costs)


def get_best_position_dist_square(crabs):
    # 1. Moving d costs (d+1)*d/2
    #
    # 2. Computing the minimal cost with a square cost: C = d²
    #    can be done:
    #       F(x) = (p1 - x)² + (p2 - x)² + ... + (pn - x)²
    #       F(x) = nx² - 2x(p1 + p2 + ... + pn) + (p1² + p2² + ... + pn²)
    #       F²(x) = 2nx - 2(p1 + p2 + ... + pn)
    #       F'(x) = 0 <=> x = (p1 + ... + pn) / n
    #
    # 3. Using the best solution for problem 2 works for problem 2 but I don't know why
    crabs = sorted(crabs)
    n = len(crabs)
    x = sum(crabs) / len(crabs)
    costs = []
    for cand in math.floor(x), math.ceil(x):
        distances = [abs(crab-cand) for crab in crabs]
        cost = sum([d*(d+1)//2 for d in distances])
        costs.append(cost)
    return min(costs)

def run_tests():
    crabs = [16,1,2,0,4,2,7,1,2,14]
    assert get_best_position(crabs) == 37
    assert get_best_position_dist_square(crabs) == 168

def get_solutions():
    crabs = get_crabs_from_file()
    print(get_best_position(crabs))
    print(get_best_position_dist_square(crabs))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
