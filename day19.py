# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re

scanner_re = r"^--- scanner (\d+) ---$"


def get_info_from_lines(lines):
    scanner = None
    info = []
    scanner_info = []
    for l in lines:
        if scanner is None:
            m = re.match(scanner_re, l)
            scanner = int(m.group(1))
            assert scanner == len(info)
        elif l == "":
            info.append(scanner_info)
            scanner = None
            scanner_info = []
        else:
            pos = [int(v) for v in l.split(",")]
            scanner_info.append(pos)
    return info


def get_info_from_file(file_path="day19_input.txt"):
    with open(file_path) as f:
        return get_info_from_lines([l.strip() for l in f])


def run_tests():
    info = get_info_from_file("day19_example_input.txt")
    print(info)


def get_solutions():
    info = get_info_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
