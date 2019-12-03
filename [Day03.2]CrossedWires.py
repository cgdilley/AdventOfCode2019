from __future__ import annotations
from typing import Iterable, List, Dict, Tuple


def main():
    wire1, wire2 = load_wires()

    intersections = wire1.get_intersections(wire2)

    closest = min(intersections, key=lambda c: wire1.coords[c] + wire2.coords[c])

    print("Closest intersection: (%d, %d), with distance of %d, requiring %d combined steps."
          % (closest[0], closest[1], manhattan(closest), wire1.coords[closest] + wire2.coords[closest]))


class Wire:

    def __init__(self, coords: Iterable[Tuple[int, int]], corners: Iterable[Tuple[int, int]] = None):
        _bounds = [[0, 0], [0, 0]]
        self.coords = dict()
        step = 0
        for coord in coords:
            step += 1
            # Store coords with their minimum step distance
            if coord not in self.coords:
                self.coords[coord] = step

            # Calculating bounds is just for rendering, doesn't help solution at all
        #     if coord[0] < _bounds[0][0]:
        #         _bounds[0][0] = coord[0]
        #     if coord[0] > _bounds[1][0]:
        #         _bounds[1][0] = coord[0]
        #     if coord[1] < _bounds[0][1]:
        #         _bounds[0][1] = coord[1]
        #     if coord[1] > _bounds[1][1]:
        #         _bounds[1][1] = coord[1]
        #
        # self.bounds = (tuple(_bounds[0]), tuple(_bounds[1]))
        # self.corners = corners

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
        # corners = []
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
            # corners.append(position)
        # return Wire(coords, corners=corners)
        return Wire(coords)


def load_wires() -> Tuple[Wire, Wire]:
    with open("input/input03.txt", "r") as f:
        lines = [[x.strip() for x in line.split(",")] for line in f.readlines()]

    return Wire.read_instructions(lines[0]), Wire.read_instructions(lines[1])


def manhattan(pos: Tuple[int, int]):
    return abs(pos[0]) + abs(pos[1])

#
# def render_wires(*wires: Wire) -> str:
#     wires = list(wires)
#     drawing = ""
#     # Obviously not the most efficient to do 4 loops, but idgaf
#     bounds = ((
#                   min([w.bounds[0][0] for w in wires]),
#                   min([w.bounds[1][0] for w in wires])
#               ),
#               (
#                   max([w.bounds[0][1] for w in wires]),
#                   max([w.bounds[1][1] for w in wires])
#               ))
#
#     intersections = set()
#     for i, w1 in enumerate(wires):
#         for j, w2 in enumerate(wires[i+1:]):
#             intersections = intersections.union(w1.get_intersections(w2))
#
#     coords = set()
#     corners = set()
#     for wire in wires:
#         coords = coords.union(wire.coords)
#         corners = corners.union(wire.corners)
#
#     for y in range(bounds[0][1], bounds[1][1]):
#         for x in range(bounds[0][0], bounds[1][0]):
#             char = "."
#             if (x, y) in intersections:
#                 char = "X"
#


if __name__ == "__main__":
    main()
