from typing import List, Optional, Dict


def main():
    orig = load()

    for noun in range(100):
        for verb in range(100):
            instructions = [x for x in orig]
            replace(instructions, {1: noun, 2: verb})
            result = run_program(instructions)

            print("[N=%d, V=%d] - Program halted with %s status.  Value in position 0 = %d" %
                  (noun, verb, "HALT" if result else "CRASH", instructions[0]))
            if instructions[0] == 19690720:
                print("100 * NOUN + VERB = %d" % ((100 * noun) + verb))
                return


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

    parameters = instructions[pos+1:pos+4]
    val1 = instructions[parameters[0]]
    val2 = instructions[parameters[1]]

    if code == 1:
        instructions[parameters[2]] = val1 + val2
        return pos + 4
    elif code == 2:
        instructions[parameters[2]] = val1 * val2
        return pos + 4
    else:
        raise Exception("Invalid opcode '%d'" % code)


if __name__ == "__main__":
    main()
