from shared.Intcode import Computer
from typing import List, Optional, Dict


def main():
    computer = load()
    orig = computer.registers

    for noun in range(100):
        for verb in range(100):
            computer.pos = 0
            computer.registers = [x for x in orig]
            replace(computer, {1: noun, 2: verb})
            result = run_program(computer)

            print("[N=%d, V=%d] - Program halted with %s status.  Value in position 0 = %d" %
                  (noun, verb, "HALT" if result else "CRASH", computer.registers[0]))
            if computer.registers[0] == 19690720:
                print("100 * NOUN + VERB = %d" % ((100 * noun) + verb))
                return


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
