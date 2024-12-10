import functools
import itertools
import math


def _parse_input(lines):
    lines = [line.split(":") for line in lines]
    lines = [(int(result), tuple(int(o) for o in operands.strip().split())) for result, operands in lines]
    return lines


def mul(a, b):
    return a * b


def add(a, b):
    return a + b


def concat(a, b):
    return int(str(a) + str(b))


def puzzle1(lines):
    equations = _parse_input(lines)
    grand_total = 0
    for result, operands in equations:
        n_operands = (len(operands) - 1)
        combination = 0
        possible = False
        while combination < math.pow(2, n_operands):
            total = operands[0]
            for i in range(n_operands):
                if (combination >> i) & 1 == 0:
                    total += operands[i + 1]
                else:
                    total *= operands[i + 1]

            if result == total:
                possible = True
                break

            combination += 1

        if possible:
            grand_total += result

    # 3351424677624
    return grand_total


def puzzle2(lines):
    equations = _parse_input(lines)
    grand_total = 0
    for result, operands in equations:
        n_operands = len(operands) - 1
        possible = False
        for combination in itertools.product([add, mul, concat], repeat=n_operands):
            total = operands[0]

            for i, operator in enumerate(combination):
                total = operator(total, operands[i + 1])

                if total > result:
                    break

            if result == total:
                possible = True
                break

        if possible:
            grand_total += result

    # 204976636995111
    return grand_total
