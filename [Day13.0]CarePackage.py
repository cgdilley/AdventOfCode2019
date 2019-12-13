from shared.Intcode import Computer

from typing import List, Tuple, Dict, Optional, Union


def main():
    computer = load()

    screen = draw_game_screen(computer)

    blocks = len([x for x in screen.values() if x == 2])

    bounds = (max((x for x in screen.keys()), key=lambda c: c[0])[0],
              max((y for y in screen.keys()), key=lambda c: c[1])[1])

    print("The final screen has %d blocks. " % blocks)


#


def load() -> Computer:
    with open("input/input13.txt", "r") as f:
        return Computer.from_string(f.read())


#


def draw_game_screen(computer: Computer) -> Dict[Tuple[int, int], int]:
    screen = dict()
    while True:
        outputs = computer.run_until_outputs(3)
        if outputs is None:
            break
        screen[(outputs[0], outputs[1])] = outputs[2]
    return screen

#


#


if __name__ == "__main__":
    main()
