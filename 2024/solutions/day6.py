import copy
import pprint


def _parse_input(lines):
    # so I can change stuff
    return [[position for position in line] for line in lines]


GUARD_FACES = "<^>v"


def _find_guard(map):
    for r, line in enumerate(map):
        for c, position in enumerate(line):
            if position in GUARD_FACES:
                return r, c


def _move(map, guard_pos) -> tuple[tuple[int, int], bool]:
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
        if map[new_pos_x][new_pos_y] in "#O":
            curr_idx = GUARD_FACES.index(guard)
            map[guard_pos[0]][guard_pos[1]] = GUARD_FACES[(curr_idx + 1) % len(GUARD_FACES)]
            return guard_pos, (new_pos_x, new_pos_y)
    except IndexError:
        pass

    return (new_pos_x, new_pos_y), None


def puzzle1(lines):
    map = _parse_input(lines)
    guard = _find_guard(map)

    visited = set()

    out = False
    while not out:
        visited.add(guard)
        (new_pos_x, new_pos_y), collision = _move(map, guard)
        if collision:
            continue
        elif not (0 <= new_pos_x < len(map)) or not (0 <= new_pos_y < len(map[0])):
            out = True
        else:
            map[new_pos_x][new_pos_y] = map[guard[0]][guard[1]]
            map[guard[0]][guard[1]] = "."
            guard = new_pos_x, new_pos_y

    # 4977
    return len(visited)


def puzzle2(lines):
    original_map = _parse_input(lines)
    map = copy.deepcopy(original_map)
    original_guard = _find_guard(map)

    count = 0
    for i in range(len(original_map)):
        for j in range(len(original_map[0])):
            if original_map[i][j] == "#" or original_map[i][j] in GUARD_FACES:
                continue

            map = copy.deepcopy(original_map)
            map[i][j] = "O"
            collision_spots = [(i + dx, j + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if abs(dx) != abs(dy)]
            guard = original_guard

            collisions = set()
            start_gather_collisions = False

            loop = False
            while not loop:
                new_pos, collision_wall = _move(map, guard)
                new_pos_x, new_pos_y = new_pos

                if collision_wall:
                    if collision_wall == (i, j) and new_pos in collision_spots:
                        start_gather_collisions = True
                    if start_gather_collisions:
                        if (guard, collision_wall) in collisions:
                            loop = True
                        collisions.add((guard, collision_wall))

                elif not (0 <= new_pos_x < len(map)) or not (0 <= new_pos_y < len(map[0])):
                    break
                else:
                    map[new_pos_x][new_pos_y] = map[guard[0]][guard[1]]
                    map[guard[0]][guard[1]] = "."
                    guard = new_pos_x, new_pos_y

            if loop:
                count += 1

    # 1732 high
    return count
