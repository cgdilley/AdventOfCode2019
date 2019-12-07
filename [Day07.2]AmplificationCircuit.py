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
    sequence_scores = {x: None for x in permutations(range(amplifiers, amplifiers * 2))}

    for curr_sequence in sequence_scores.keys():

        # Instantiate the computers
        computers = [Computer(copy_registers(registers), inputs=[curr_sequence[amp_number]])
                     for amp_number in range(amplifiers)]

        # Track their outputs
        outputs = {i: [] for i in range(amplifiers)}

        # Starting from the first amplifier, feed in the appropriate input and run until producing an output.
        # Then move to the next amplifier in the loop, feeding that output as the next input.  Continue until
        # the final amplifier halts, then read the final input value from the last amplifier
        curr_computer = 0
        input_val = 0
        while True:
            computers[curr_computer].inputs.append(input_val)
            input_val = computers[curr_computer].run_until_output()

            # Getting a value of None back from Computer.run_until_output() indicates that the program halted
            if input_val is None:
                if curr_computer == amplifiers - 1:
                    break
            else:
                outputs[curr_computer].append(input_val)
            curr_computer = (curr_computer + 1) % amplifiers

        sequence_scores[curr_sequence] = outputs[amplifiers - 1][-1]

    return max([(k, v) for k, v in sequence_scores.items()], key=lambda x: x[1])


#


def copy_registers(registers: List[int]) -> List[int]:
    return [x for x in registers]


#


if __name__ == "__main__":
    main()
