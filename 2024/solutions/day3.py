
import re


def puzzle1(lines):
    mul_pattern = re.compile(r"mul\(\d+,\d+\)")
    numbers_patter = re.compile(r"(\d+),(\d+)")
    total = 0
    for line in lines:
        mul_matches = mul_pattern.finditer(line)
        for mul_match in mul_matches:
            regs = mul_match.regs[0]
            mul = line[regs[0]:regs[1]]
            nums = numbers_patter.findall(mul)
            nums = nums[0]
            total += int(nums[0]) * int(nums[1])

    # 183669043
    return total


def puzzle2(lines):
    ops_pattern = re.compile(r"(?:mul\(\d+,\d+\))|(?:do\(\))|(?:don't\(\))")
    numbers_pattern = re.compile(r"(\d+),(\d+)")
    total = 0
    mul_enabled = True
    for line in lines:
        ops_matches = ops_pattern.finditer(line)
        for op_match in ops_matches:
            regs = op_match.regs[0]
            if line[regs[0]:].startswith("do("):
                mul_enabled = True
            elif line[regs[0]:].startswith("don"):
                mul_enabled = False
            elif mul_enabled:
                mul = line[regs[0]:regs[1]]
                nums = numbers_pattern.findall(mul)
                nums = nums[0]
                total += int(nums[0]) * int(nums[1])

    # 59097164
    return total
