from __future__ import annotations
from typing import Iterable, List, Dict, Tuple
from shared.day3 import load_wires, manhattan, Wire


def main():
    wire1, wire2 = load_wires()

    intersections = wire1.get_intersections(wire2)

    closest = min(intersections, key=lambda c: wire1.coords[c] + wire2.coords[c])

    print("Closest intersection: (%d, %d), with distance of %d, requiring %d combined steps."
          % (closest[0], closest[1], manhattan(closest), wire1.coords[closest] + wire2.coords[closest]))


if __name__ == "__main__":
    main()
