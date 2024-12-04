import re


def _transpose(M):
    return ["".join(M[j][i] for j in range(len(M))) for i in range(len(M[0]))]


def _diagonals(M):
    # top left to bottom right
    upper_diagonals = ["".join(M[i-j][j] for j in range(i + 1)) for i in range(len(M))]
    lower_diagonals = ["".join(M[len(M)-1-j][1+i+j] for j in range(len(M) - 1 - i)) for i in range(len(M) - 1)]

    return upper_diagonals + lower_diagonals


def _diagonals2(M):
    # top right to bottom left
    upper_diagonals = ["".join(M[i-j][len(M)-1-j] for j in range(i + 1)) for i in range(len(M))]
    lower_diagonals = ["".join(M[len(M)-1-j][len(M)-1-(1+i+j)] for j in range(len(M) - 1 - i)) for i in range(len(M) - 1)]

    return upper_diagonals + lower_diagonals


def puzzle1(lines):
    xmas_pat = re.compile("XMAS")
    samx_pat = re.compile("SAMX")

    count_lines = sum(len(xmas_pat.findall(line)) + len(samx_pat.findall(line)) for line in lines)
    count_columns = sum(len(xmas_pat.findall(line)) + len(samx_pat.findall(line)) for line in _transpose(lines))
    count_diagonals = sum(len(xmas_pat.findall(line)) + len(samx_pat.findall(line)) for line in _diagonals(lines))
    count_diagonals2 = sum(len(xmas_pat.findall(line)) + len(samx_pat.findall(line)) for line in _diagonals2(lines))

    # 2344
    return count_lines + count_columns + count_diagonals + count_diagonals2


def puzzle2(lines):
    count = 0
    for i in range(1, len(lines) - 1):
        for j in range(1, len(lines) - 1):
            if lines[i][j] == "A":
                top_left = lines[i-1][j-1]
                bottom_right = lines[i+1][j+1]

                cross1 = top_left in "MS" and bottom_right in "MS" and top_left != bottom_right

                top_right = lines[i - 1][j + 1]
                bottom_left = lines[i + 1][j - 1]

                cross2 = top_right in "MS" and bottom_left in "MS" and top_right != bottom_left

                if cross1 and cross2:
                    count += 1

    # 1815
    return count
