
def _parse_input(lines):
    return [[int(level) for level in report.split()] for report in lines]


def _test_report(report) -> bool:
    diffs = list(a - b for a, b in zip(report, report[1:]))
    increasing = sum(1 for d in diffs if d > 0)
    abses = list(abs(d) for d in diffs)
    return min(abses) >= 1 and max(abses) <= 3 and (len(diffs) == increasing or increasing == 0)


def puzzle1(lines):
    reports = _parse_input(lines)

    # 442
    return sum(1 for report in reports if _test_report(report))


def puzzle2(lines):
    reports = _parse_input(lines)

    safe_count = 0
    for report in reports:
        safe = _test_report(report)
        if safe:
            safe_count += 1
        else:
            for i in range(len(report)):
                if _test_report(report[:i] + report[i+1:]):
                    safe_count += 1
                    break

    # 493
    return safe_count
