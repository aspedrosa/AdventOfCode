
def _parse_input(lines):
    separator = lines.index("")

    rules = lines[:separator]
    rules = [tuple(int(n) for n in r.split("|")) for r in rules]
    infront = {}
    for b, f in rules:
        if b not in infront:
            infront[b] = []
        infront[b].append(f)
    rules = infront
    updates = lines[separator + 1:]
    updates = [list(int(n) for n in u.split(",")) for u in updates]

    return rules, updates


def _correct_order(rules, update):
    # tuple[bool, tuple[Optional[int], Optional[int]]]
    # bool tels if its correct order or not. if true, both ints are None
    # if false, ints indicate the indexes of elements that are in wrong order

    for i, e in enumerate(update[1:]):
        if not (must_be_in_front := rules.get(e)):
            continue

        # lets go iterate backward to check if there are numbers that should be on front
        for j, e_backwards in enumerate(update[:i + 1]):
            if e_backwards in must_be_in_front:
                return False, (i + 1, j)

    return True, (None, None)


def puzzle1(lines):
    rules, updates = _parse_input(lines)

    total = 0
    for update in updates:
        correct_order, _ = _correct_order(rules, update)
        if correct_order:
            total += update[len(update) // 2]

    # 5275
    return total


def puzzle2(lines):
    rules, updates = _parse_input(lines)

    total = 0
    for update in updates:
        correct_order, (i, j) = _correct_order(rules, update)
        if not correct_order:
            while not correct_order:
                # swap elements that are wrong. lets hope that cicles wont exist. maybe its impossible for them to exist
                tmp = update[i]
                update[i] = update[j]
                update[j] = tmp

                correct_order, (i, j) = _correct_order(rules, update)

            total += update[len(update) // 2]

    # 6191
    return total
