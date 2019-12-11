from shared.Intcode import Computer

from typing import Dict, Tuple


def main():
    computer = load()

    surface = run_painting(computer, start_color=0)

    print("Painted %d squares at least once." % len(surface))


def load() -> Computer:
    with open("input/input11.txt", "r") as f:
        return Computer.from_string(f.read())


def run_painting(computer: Computer, start_color: int) -> Dict[Tuple[int, int], int]:
    robot_coord = (0, 0)
    direction = (0, -1)
    surface = dict()
    computer.inputs.append(start_color)
    while True:
        color = computer.run_until_output()
        if color is None:
            break
        surface[robot_coord] = color

        turn_direction = computer.run_until_output()
        if turn_direction is None:
            break
        direction = turn(direction, turn_direction)
        robot_coord = tuple((robot_coord[0] + direction[0], robot_coord[1] + direction[1]))

        computer.inputs.append(get_surface_color(surface, robot_coord))

    return surface


def get_surface_color(surface: Dict[Tuple[int, int], int], pos: Tuple[int, int]) -> int:
    return surface[pos] if pos in surface else 0


def turn(curr: Tuple[int, int], turn_direction: int) -> Tuple[int, int]:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    index = directions.index(curr)
    index += 1 if turn_direction == 1 else -1
    return directions[index % 4]


#


#


if __name__ == "__main__":
    main()
