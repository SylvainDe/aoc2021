# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import functools
import itertools
import collections

def get_fishes_from_file(file_path="day6_input.txt"):
    with open(file_path) as f:
        for l in f:
            return [int(v) for v in l.strip().split(",")]



def one_generation(fishes):
    c = fishes.count(0)
    fishes = [n-1 if n else 6 for n in fishes]
    return fishes + [8] * c

def n_generations(fishes, n):
    # There must be a faster way
    for _ in range(n):
        fishes = one_generation(fishes)
    return fishes


@functools.lru_cache(maxsize=100000)
def nb_fishes_from_fish(fish, n):
    if n == 0 or fish > n:
        return 1
    if fish == 0:
        return nb_fishes_from_fish(6, n-1) + nb_fishes_from_fish(8, n-1)
    return nb_fishes_from_fish(0, n - fish)


def nb_fishes_from_fishes(fishes, n):
     return sum(nb * nb_fishes_from_fish(val, n)
                for val, nb in collections.Counter(fishes).items())


def run_tests():
    fishes1 = [3, 4, 3, 1, 2]
    fishes2 = one_generation(fishes1)
    assert fishes2 == [2,3,2,0,1]
    fishes3 = one_generation(fishes2)
    assert fishes3 == [1,2,1,6,0,8]
    assert n_generations(fishes1, 2) == [1,2,1,6,0,8]
    assert n_generations(fishes1, 3) == [0,1,0,5,6,7,8]
    assert n_generations(fishes1, 4) == [6,0,6,4,5,6,7,8,8]
    assert n_generations(fishes1, 5) == [5,6,5,3,4,5,6,7,7,8]
    assert n_generations(fishes1, 6) == [4,5,4,2,3,4,5,6,6,7]
    assert n_generations(fishes1, 18) == [6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8]
    print(nb_fishes_from_fishes(fishes1, 256) == 26984457539)

def get_solutions():
    fishes = get_fishes_from_file()
    print(nb_fishes_from_fishes(fishes, 256))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
