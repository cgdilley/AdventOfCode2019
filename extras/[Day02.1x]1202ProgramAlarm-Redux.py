from shared.Intcode import Computer
from typing import List, Optional, Dict


def main():
    computer = load()
    replace(computer, {1: 12, 2: 2})
    result = run_program(computer)

    print("Program halted with %s status.  Value in position 0 = %d" %
          ("HALT" if result else "CRASH", computer.registers[0]))


def load() -> Computer:
    with open("../input/input02.txt", "r") as f:
        return Computer.from_string(f.read())


def replace(computer: Computer, replacements: Dict[int, int]):
    for pos, val in replacements.items():
        computer.registers[pos] = val


def run_program(computer: Computer) -> bool:
    try:
        computer.run()
        return True
    except Exception as e:
        print(str(e))
        return False


if __name__ == "__main__":
    main()
