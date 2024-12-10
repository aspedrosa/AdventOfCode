
def _parse_input(lines):
    lines = [l.split() for l in lines]
    lines = [(int(l1), int(l2)) for l1, l2 in lines]
    return zip(*lines)


def puzzle1(lines):
    l1, l2 = _parse_input(lines)
    l1, l2 = list(l1), list(l2)

    l1.sort()
    l2.sort()

    total = sum(abs(l1 - l2) for l1, l2 in zip(l1, l2))

    # 1388114
    return total


def puzzle2(lines):
    left, right = _parse_input(lines)

    total_score = 0
    count_cache = {}
    for l in left:
        if l not in count_cache:
            count_cache[l] = right.count(l)
        total_score += l * count_cache[l]

    # 23529853
    return total_score
