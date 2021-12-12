# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_map_item_from_line(l, sep="-"):
    a, b, c = l.partition(sep)
    assert b == sep
    return (a, c)


def get_map_from_lines(lines):
    return [get_map_item_from_line(l.strip()) for l in lines]


def get_map_from_file(file_path="day12_input.txt"):
    with open(file_path) as f:
        return get_map_from_lines(f)


def build_graph(map_):
    graph = dict()
    for a, b in map_:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def get_nb_paths(graph, start="start", end="end"):
    # I suspect there is a much better way using dynamic programming
    nb_path = 0
    paths = collections.deque([[start]])
    while paths:
        path = paths.popleft()
        last = path[-1]
        if last == end:
            nb_path += 1
        # print(last)
        for succ in graph.get(last, set()):
            # print(last, succ)
            if succ.isupper() or succ not in path:
                paths.append(path + [succ])
    return nb_path


def run_tests():
    map_ = [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ]
    map_ = get_map_from_lines(map_)
    graph = build_graph(map_)
    assert get_nb_paths(graph) == 10


def get_solutions():
    map_ = get_map_from_file()
    graph = build_graph(map_)
    print(get_nb_paths(graph))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
