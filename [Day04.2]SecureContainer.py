from typing import Tuple, List
import math


def main():
    lower, upper = load_range()

    numbers = []

    num = lower - 1
    # digits = _get_digits(num)
    while True:
        num = find_next_number(num)
        if num > upper:
            break
        numbers.append(num)

    print("Found %d numbers meeting the criteria." % len(numbers))


def load_range() -> Tuple[int, int]:
    with open("input/input04.txt", "r") as f:
        return tuple(int(x.strip()) for x in f.read().split("-"))


def _get_digits(num: int) -> List[int]:
    return [int(c) for c in str(num)]


def _get_number(digits: List[int]) -> int:
    num = 0
    for i, d in enumerate(digits):
        num += d * (10 ** (len(digits) - i - 1))
    return num


def find_next_number(num: int) -> int:
    digits = _get_digits(num)
    digits = find_next_digits(digits)
    return _get_number(digits)


def find_next_digits(digits: List[int]) -> List[int]:
    digits = [d for d in digits]
    duplicates = False
    while not duplicates:
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                break
            else:
                digits[i] = 0

        carryover_digit = None
        for i in range(len(digits) - 1):
            if carryover_digit is not None:
                digits[i+1] = carryover_digit
            elif digits[i] > digits[i+1]:
                digits[i+1] = digits[i]
                carryover_digit = digits[i]

        duplicates = False
        i = 0
        while i < len(digits) - 1:
            d = digits[i]
            streak = 1
            for j in range(i+1, len(digits)):
                if digits[j] == d:
                    streak += 1
                else:
                    break
            if streak == 2:
                duplicates = True
                break
            i += streak

    return digits


if __name__ == "__main__":
    main()
