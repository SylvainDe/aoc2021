# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections

def get_diag_from_file(file_path="day3_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


other_bit = { "0": "1", "1": "0" }


def get_power_consumption(diagnostic):
    gamma, epsilon = "", ""
    for i in range(len(diagnostic[0])):
        c = collections.Counter(diag[i] for diag in diagnostic)
        val, nb = c.most_common(1)[0]
        gamma += val
        epsilon += other_bit[val]
    return int(gamma, base=2) * int(epsilon, base=2)


def run_tests():
    diag = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    print(get_power_consumption(diag))


def get_solutions():
    diag = get_diag_from_file()
    print(get_power_consumption(diag))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
