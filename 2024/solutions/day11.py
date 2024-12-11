
def _parse_input(lines):
    return lines[0].split()

def _perform_algorightm(line, iterations):
    new_line = line[:]
    for _ in range(iterations):
        new_stones = []
        for i, stone in enumerate(new_line):
            if stone == "0":
                new_line[i] = "1"
            elif int(stone) > 9 and len(stone) % 2 == 0:
                new_line[i] = stone[:len(stone) // 2]
                new_stones.append(str(int(stone[len(stone) // 2:])))
            else:
                new_line[i] = str(int(stone) * 2024)

        new_line.extend(new_stones)

    return len(new_line)

def puzzle1(lines):
    line = _parse_input(lines)

    count = _perform_algorightm(line, 25)

    # 224529
    return count


def puzzle2(lines):
    original_line = _parse_input(lines)

    line = [1]
    count_when_zero = [1, 1]
    zeros = []
    for iteration in range(75):
        print(iteration)
        new_stones = []
        zero_count = 0
        for i, stone in enumerate(line):
            if stone == "0":
                zero_count += 1
            elif int(stone) > 9 and len(stone) % 2 == 0:
                line[i] = stone[:len(stone) // 2]
                new_stones.append(str(int(stone[len(stone) // 2:])))
            else:
                line[i] = str(int(stone) * 2024)
        if zero_count > 0:
            zeros.append((zero_count, 0))
        line = [stone for stone in line if stone != "0"] + new_stones
        total_count = len(line) + sum(count_when_zero[iteration_for_zero] * zero_count for zero_count, iteration_for_zero in zeros)
        zeros = [(zero_count, iteration_for_zero + 1) for zero_count, iteration_for_zero in zeros]
        count_when_zero.append(total_count)

    total_count = 0
    for iteration in range(75):
        new_stones = []
        for i, stone in enumerate(line):
            if stone == "0":
                total_count += count_when_zero[75 - iteration - 1]
            elif int(stone) > 9 and len(stone) % 2 == 0:
                line[i] = stone[:len(stone) // 2]
                new_stones.append(str(int(stone[len(stone) // 2:])))
            else:
                line[i] = str(int(stone) * 2024)

        line = [stone for stone in line if stone != "0"] + new_stones

    #
    return len(line)
