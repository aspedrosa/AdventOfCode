
def _parse_input(lines):
    return [int(entry) for entry in lines[0]]


def puzzle1(lines):
    disk_map = _parse_input(lines)

    file_system = []
    right_i = len(disk_map) - 1
    if right_i % 2 != 0:
        right_i -= 1
    missing_from_right_i = disk_map[right_i]
    for left_i, size in enumerate(disk_map):
        if left_i > right_i:
            break
        if left_i % 2 == 0:  # file
            if left_i == right_i:
                size = missing_from_right_i
                missing_from_right_i = 0

            for _ in range(size):
                file_system.append(left_i // 2)
        else:  # free space
            for _ in range(size):
                if missing_from_right_i == 0:
                    right_i -= 2

                    if right_i < left_i:
                        missing_from_right_i = 0
                        continue

                    missing_from_right_i = disk_map[right_i]

                file_system.append(right_i // 2)
                missing_from_right_i -= 1

    checksum = sum(i * id for i, id in enumerate(file_system))

    # 6211348208140
    return checksum


def _merge_free_space(filesystem, free_space_idx, moved_file_size):
    new_filesystem = filesystem[:free_space_idx - 1]
    is_file1, size1, _ = filesystem[free_space_idx - 1]
    free_space_size = moved_file_size
    if is_file1:
        new_filesystem.append(filesystem[free_space_idx - 1])
    else:
        free_space_size += size1
    try:
        is_file2, size2, _ = filesystem[free_space_idx + 1]
    except IndexError:
        is_file2 = False
    else:
        if not is_file2:
            free_space_size += size2

    new_filesystem.append((False, free_space_size, None))
    if is_file2:
        new_filesystem.append(filesystem[free_space_idx + 1])

    new_filesystem.extend(filesystem[free_space_idx + 2:])

    return new_filesystem


def puzzle2(lines):
    disk_map = _parse_input(lines)

    filesystem = [(i % 2 == 0, size, i // 2) for i, size in enumerate(disk_map)]

    right_i_file = len(filesystem) - 1
    if not filesystem[right_i_file][0]:
        right_i_file -= 1
    left_i_free_space_i = 1
    while right_i_file > left_i_free_space_i:
        is_file, f_size, file_id = filesystem[right_i_file]
        if not is_file:
            right_i_file -= 1
            continue

        free_space_i = left_i_free_space_i
        while free_space_i < right_i_file:
            is_file, fs_size, _ = filesystem[free_space_i]
            if is_file or fs_size == 0:
                free_space_i += 1
                continue

            if f_size <= fs_size:
                filesystem = _merge_free_space(filesystem, right_i_file, f_size)
                if f_size == fs_size:
                    filesystem[free_space_i] = (True, fs_size, file_id)
                elif f_size < fs_size:
                    filesystem = filesystem[:free_space_i] + [(True, f_size, file_id), (False, fs_size - f_size, None)] + filesystem[free_space_i + 1:]

                if free_space_i == left_i_free_space_i:
                    while True:
                        left_i_free_space_i += 1
                        is_file, _, _ = filesystem[left_i_free_space_i]
                        if not is_file:
                            break

                break

            free_space_i += 1

        right_i_file -= 1

    #for is_file, size, file_id in filesystem:
    #    if is_file:
    #        for _ in range(size):
    #            print(file_id, end="")
    #    else:
    #        for _ in range(size):
    #            print(".", end="")
    #print()

    i = 0
    checksum = 0
    for is_file, size, file_id in filesystem:
        if is_file:
            #checksum = size * (i + (i + size - 1)) / 2 * file_id
            #i += size
            for _ in range(size):
                checksum += i * file_id
                i += 1
        else:
            i += size

    # 6239712239037 low
    return checksum
