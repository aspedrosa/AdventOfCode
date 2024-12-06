
def _parse_input(lines):
    # so I can change stuff
    return [[position for position in line] for line in lines]


GUARD_FACES = "<^>v"


def _move(map, guard_pos) -> tuple[int, int]:
    guard = map[guard_pos[0]][guard_pos[1]]

    match guard:
        case "<":
            movement = (0, -1)
        case "^":
            movement = (-1, 0)
        case ">":
            movement = (0, 1)
        case "v":
            movement = (1, 0)

    new_pos_x, new_pos_y = guard_pos[0] + movement[0], guard_pos[1] + movement[1]

    # TODO instead of moving just one by one, move until hit a wall of find a #
    try:
        if map[new_pos_x][new_pos_y] == "#":
            curr_idx = GUARD_FACES.index(guard)
            map[guard_pos[0]][guard_pos[1]] = GUARD_FACES[(curr_idx + 1) % len(GUARD_FACES)]
            return _move(map, guard_pos)
    except IndexError:
        pass

    return new_pos_x, new_pos_y


def puzzle1(lines):
    map = _parse_input(lines)
    for r, line in enumerate(map):
        for c, position in enumerate(line):
            if position in GUARD_FACES:
                guard = (r, c)

    visited = set()

    out = False
    while not out:
        visited.add(guard)
        new_pos_x, new_pos_y = _move(map, guard)
        if not (0 <= new_pos_x < len(map)):
            out = True
        elif not (0 <= new_pos_y < len(map[0])):
            out = True
        else:
            map[new_pos_x][new_pos_y] = map[guard[0]][guard[1]]
            map[guard[0]][guard[1]] = "."
            guard = new_pos_x, new_pos_y

    # 4977
    return len(visited)


def puzzle2(lines):
    map = _parse_input(lines)

    #
    return
