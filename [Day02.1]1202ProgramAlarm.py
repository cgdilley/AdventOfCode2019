from typing import List, Optional, Dict


def main():
    instructions = load()
    replace(instructions, {1: 12, 2: 2})
    result = run_program(instructions)

    print("Program halted with %s status.  Value in position 0 = %d" %
          ("HALT" if result else "CRASH", instructions[0]))


def load() -> List[int]:
    with open("input/input02.txt", "r") as f:
        return [int(x.strip()) for x in f.read().split(",")]


def replace(instructions: List[int], replacements: Dict[int, int]):
    for pos, val in replacements.items():
        instructions[pos] = val


def run_program(instructions: List[int]) -> bool:
    pos = 0
    while True:
        try:
            pos = read_opcode(instructions, pos)
            if pos is None:
                return True
        except Exception as e:
            print(str(e))
            return False


def read_opcode(instructions: List[int], pos: int) -> Optional[int]:
    code = instructions[pos]
    if code == 99:
        return None

    inp = instructions[pos+1:pos+4]
    val1 = instructions[inp[0]]
    val2 = instructions[inp[1]]

    if code == 1:
        instructions[inp[2]] = val1 + val2
        return pos + 4
    elif code == 2:
        instructions[inp[2]] = val1 * val2
        return pos + 4
    else:
        raise Exception("Invalid opcode '%d'" % code)


if __name__ == "__main__":
    main()
