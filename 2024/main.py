import importlib
import os.path

SAMPLE = False
DAY = 1
PUZZLE = 2


def main():
    directory = "samples" if SAMPLE else "inputs"
    with open(os.path.join(directory, f"day{DAY}.txt")) as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l]

    solution_module = importlib.import_module(f"solutions.day{DAY}")
    solution_function = getattr(solution_module, f"puzzle{PUZZLE}")

    solution_function(lines)


if __name__ == '__main__':
    main()