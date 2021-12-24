# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math 
import itertools

def get_program_from_file(file_path="day24_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]

def get_val(alu, var_or_number):
    if var_or_number in alu:
        return alu[var_or_number]
    return int(var_or_number)

def run_program(program, input_val):
    alu = {var: 0 for var in "wxyz"}
    for line in program:
        line = line.split(" ")
        instruction = line[0]
        dest = line[1]
        if instruction == "inp":
            inp = next(input_val)
            # assert 1 <= inp <= 9
            alu[dest] = inp
        elif instruction == "add":
            alu[dest] += get_val(alu, line[2])
        elif instruction == "mul":
            alu[dest] *= get_val(alu, line[2])
        elif instruction == "div":
            a, b = alu[dest], get_val(alu, line[2])
            q = a / b
            alu[dest] = math.floor(q) if q >= 0 else math.ceil(q)
        elif instruction == "mod":
            alu[dest] %= get_val(alu, line[2])
        elif instruction == "eql":
            alu[dest] = int(alu[dest] == get_val(alu, line[2]))
        else:
            assert False
    return alu

def run_tests():
    program = [
        "inp z",
        "inp x",
        "mul z 3",
        "eql z x",
    ]
    assert run_program(program, iter([1, 3]))["z"] == 1
    assert run_program(program, iter([2, 6]))["z"] == 1
    assert run_program(program, iter([1, 2]))["z"] == 0
    assert run_program(program, iter([2, 7]))["z"] == 0

    program = [
        "inp w",
        "add z w",
        "mod z 2",
        "div w 2",
        "add y w",
        "mod y 2",
        "div w 2",
        "add x w",
        "mod x 2",
        "div w 2",
        "mod w 2",
    ]
    for i in range(16):
        res = run_program(program, iter([i]))
        i, rem = divmod(i, 2)
        assert res["z"] == rem 
        i, rem = divmod(i, 2)
        assert res["y"] == rem 
        i, rem = divmod(i, 2)
        assert res["x"] == rem 
        i, rem = divmod(i, 2)
        assert res["w"] == rem 
 

def get_solutions():
    program = get_program_from_file()
    maxi = int("9"*14)
    for i in itertools.count(maxi, -1):
        i_lst = [int(d) for d in str(i)]
        if 0 not in i_lst:
            res = run_program(program, iter(i_lst))
            if res["z"] == 0:
                print(i)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
