import itertools


def _parse_input(lines):
    return [[l for l in line] for line in lines]  # so i can changes stuff


def _add_vector(place, vector, direction, map, antinodes):
    new = (place[0] + vector[0] * direction, place[1] + vector[1] * direction)

    if 0 <= new[0] < len(map) and 0 <= new[1] < len(map[0]):  # remember that negative indexes are valid indexes in python
        antinodes.add(new)
        #map[new[0]][new[1]] = "#"


def _add_vector_while_possible(place, vector, direction, map, antinodes):
    i = 1
    while True:
        new = (place[0] + vector[0] * direction * i, place[1] + vector[1] * direction * i)

        if not (0 <= new[0] < len(map)) or not(0 <= new[1] < len(map[0])):
            break

        antinodes.add(new)
        #map[new[0]][new[1]] = "#"

        i += 1

    if i >= 2:  # if there are two antinodes after place, place is also an antinode
        antinodes.add(place)

    return i


def puzzle1(lines):
    map = _parse_input(lines)

    frequencies = dict()
    for l, line in enumerate(map):
        for c, place in enumerate(line):
            if place != ".":
                if place not in frequencies:
                    frequencies[place] = []
                frequencies[place].append((l ,c))

    antinodes = set()
    for _, locations in frequencies.items():
        for a1, a2 in itertools.combinations(locations, 2):
            diff = (a2[0] - a1[0], a2[1] - a1[1])

            _add_vector(a2, diff, 1, map, antinodes)
            _add_vector(a1, diff, -1, map, antinodes)

    #for line in map:
    #    for l in line:
    #        print(l, end="")
    #    print()

    # 329
    return len(antinodes)


def puzzle2(lines):
    map = _parse_input(lines)

    frequencies = dict()
    for l, line in enumerate(map):
        for c, place in enumerate(line):
            if place != ".":
                if place not in frequencies:
                    frequencies[place] = []
                frequencies[place].append((l ,c))

    antinodes = set()
    for _, locations in frequencies.items():
        for a1, a2 in itertools.combinations(locations, 2):
            diff = (a2[0] - a1[0], a2[1] - a1[1])

            i = _add_vector_while_possible(a2, diff, 1, map, antinodes)
            if i >= 1:  # if created at least one after a2, then a1 is also an antinode
                antinodes.add(a1)
            i = _add_vector_while_possible(a1, diff, -1, map, antinodes)
            if i >= 1:  # if created at least one after a1, then a1 is also an antinode
                antinodes.add(a2)

    #for line in map:
    #    for l in line:
    #        print(l, end="")
    #    print()

    # 1190
    return len(antinodes)
