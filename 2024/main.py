import importlib
import os.path

SAMPLE = False
DAY = 3
PUZZLE = 2


def main():
    directory = "samples" if SAMPLE else "inputs"
    try:
        f = open(os.path.join(directory, f"day{DAY}.txt"))
    except FileNotFoundError:
        if SAMPLE:
            f = open(os.path.join(directory, f"day{DAY}_puzzle{PUZZLE}.txt"))
        else:
            raise

    with f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l]

    solution_module = importlib.import_module(f"solutions.day{DAY}")
    solution_function = getattr(solution_module, f"puzzle{PUZZLE}")

    solution = solution_function(lines)

    print(solution)


if __name__ == '__main__':
    main()
