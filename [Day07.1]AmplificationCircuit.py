from shared.Intcode import Computer
from itertools import permutations

from typing import Tuple, List, Optional, Union


def main():
    registers = load()

    sequence, score = find_phase_sequence(registers, amplifiers=5)

    print("The phase sequence with the greatest output was (%s), with a value of %d." %
          (", ".join([str(d) for d in sequence]), score))


def load() -> List[int]:
    with open("input/input07.txt", "r") as f:
        return Computer.parse_registers(f.read())


def find_phase_sequence(registers: List[int], amplifiers: int) -> Tuple[Tuple[int, ...], int]:
    # Python libraries help me cheat in generating permutations :D
    sequence_scores = {x: None for x in permutations(range(amplifiers))}

    for curr_sequence in sequence_scores.keys():
        input_val = 0
        for amp_number in range(amplifiers):
            comp = Computer(copy_registers(registers), inputs=[curr_sequence[amp_number], input_val])
            outputs = comp.run()
            input_val = outputs[0]
        sequence_scores[curr_sequence] = input_val

    return max([(k, v) for k, v in sequence_scores.items()], key=lambda x: x[1])


#


def copy_registers(registers: List[int]) -> List[int]:
    return [x for x in registers]


#


if __name__ == "__main__":
    main()
