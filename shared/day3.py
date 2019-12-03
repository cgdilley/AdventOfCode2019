from __future__ import annotations
from typing import Iterable, List, Dict, Tuple


class Wire:

    def __init__(self, coords: Iterable[Tuple[int, int]], corners: Iterable[Tuple[int, int]] = None):
        self.coords = dict()
        self.raw = list(coords)
        step = 0
        for coord in coords:
            step += 1
            # Store coords with their minimum step distance
            if coord not in self.coords:
                self.coords[coord] = step

        self.total_length = step

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