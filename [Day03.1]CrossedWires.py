from __future__ import annotations
from typing import Iterable, List, Dict, Tuple


def main():
    wire1, wire2 = load_wires()

    intersections = wire1.get_intersections(wire2)

    closest = min(intersections, key=manhattan)

    print("Closest intersection: (%d, %d), with distance of %d" % (closest[0], closest[1], manhattan(closest)))


class Wire:

    def __init__(self, coords: Iterable[Tuple[int, int]]):
        _bounds = [[0, 0], [0, 0]]
        self.coords = dict()
        for coord in coords:
            self.coords[coord] = None
            if coord[0] < _bounds[0][0]:
                _bounds[0][0] = coord[0]
            if coord[0] > _bounds[1][0]:
                _bounds[1][0] = coord[0]
            if coord[1] < _bounds[0][1]:
                _bounds[0][1] = coord[1]
            if coord[1] > _bounds[1][1]:
                _bounds[1][1] = coord[1]
        self.bounds = (tuple(_bounds[0]), tuple(_bounds[1]))

    def on_wire_path(self, pos: Tuple[int, int]) -> bool:
        return pos in self.coords

    def intersects(self, wire: Wire) -> bool:
        return any([self.on_wire_path(pos) for pos in wire.coords])

    def get_intersections(self, wire: Wire) -> List[Tuple[int, int]]:
        return [pos for pos in self.coords if wire.on_wire_path(pos)]

    @staticmethod
    def read_instructions(instructions: List[str]):
        coords = []
        position = (0, 0)
        for i in instructions:
            direction = i[0]
            distance = int(i[1:])
            if direction == "D":
                coords.extend([(position[0], y + 1) for y in range(position[1], position[1] + distance)])
            elif direction == "U":
                coords.extend([(position[0], y - 1) for y in range(position[1], position[1] - distance, -1)])
            elif direction == "L":
                coords.extend([(x - 1, position[1]) for x in range(position[0], position[0] - distance, -1)])
            elif direction == "R":
                coords.extend([(x + 1, position[1]) for x in range(position[0], position[0] + distance)])
            position = coords[-1]
        return Wire(coords)


def load_wires() -> Tuple[Wire, Wire]:
    with open("input/input03.txt", "r") as f:
        lines = [[x.strip() for x in line.split(",")] for line in f.readlines()]

    return Wire.read_instructions(lines[0]), Wire.read_instructions(lines[1])


def manhattan(pos: Tuple[int, int]):
    return abs(pos[0]) + abs(pos[1])



if __name__ == "__main__":
    main()
