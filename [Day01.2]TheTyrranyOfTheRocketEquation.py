import math


def total_fuel(m: int) -> int:
    remaining = m
    total = 0
    while True:
        remaining = math.floor(remaining / 3) - 2
        if remaining <= 0:
            break
        total += remaining

    return total


with open("input/input01.txt", "r") as f:
    print(sum([total_fuel(int(m.strip())) for m in f.readlines()]))

