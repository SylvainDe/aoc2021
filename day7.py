# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


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
        print(pos, cost)
        costs.append(cost)
    return min(costs)


def run_tests():
    crabs = [16,1,2,0,4,2,7,1,2,14]
    assert get_best_position(crabs) == 37

def get_solutions():
    crabs = get_crabs_from_file()
    print(get_best_position(crabs))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
