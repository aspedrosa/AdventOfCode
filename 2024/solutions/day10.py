
def _parse_input(lines):
    return [[int(e) for e in line] for line in lines]

def _check_around(row, column, i, map):
    goods = []
    for diff_r, diff_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_r = row + diff_r
        new_c = column + diff_c
        if not (0 <= new_r < len(map)) or not (0 <= new_c < len(map[0])):
            continue  # skip invalid map positions

        if map[new_r][new_c] - i == 1:
            goods.append((new_r, new_c, i + 1))

    return goods


def puzzle1(lines):
    map = _parse_input(lines)

    scores = []
    for r, line in enumerate(map):
        for c, element in enumerate(line):
            if element != 0:
                continue

            nines_visited = set()
            stack = [(r, c, 0)]
            while stack:
                row, column, i = stack.pop()
                if i == 9:
                    nines_visited.add((row, column))
                    continue

                stack.extend(_check_around(row, column, i, map))

            scores.append(len(nines_visited))

    # 737
    return sum(scores)


def puzzle2(lines):
    map = _parse_input(lines)

    scores = []
    for r, line in enumerate(map):
        for c, element in enumerate(line):
            if element != 0:
                continue

            score = 0
            stack = [(r, c, 0)]
            while stack:
                row, column, i = stack.pop()
                if i == 9:
                    score += 1
                    continue

                stack.extend(_check_around(row, column, i, map))

            scores.append(score)

    # 1619
    return sum(scores)
