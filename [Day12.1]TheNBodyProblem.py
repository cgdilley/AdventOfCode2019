from __future__ import annotations
import re

from typing import Tuple, List, Dict, Optional, Union, Iterable


def main():
    moons = load()

    run_simulation(moons, steps=1000)

    total_energy = sum(m.total_energy() for m in moons)
    print("The total energy in the system after 1000 steps is: %d" % total_energy)


def load() -> List[Moon]:
    regex = re.compile(r'<x=([\-\d]+), y=([\-\d]+), z=([\-\d]+)>')
    moons = []
    with open("input/input12.txt", "r") as f:
        for line in f.readlines():
            m = regex.match(line.strip())
            moons.append(Moon(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return moons

#


def run_simulation(moons: List[Moon], steps: int):
    for step in range(steps):
        for i, m1 in enumerate(moons[:-1]):
            for m2 in moons[i+1:]:
                Moon.gravitate(m1, m2)
        for m in moons:
            m.move()


#


class Moon:

    def __init__(self, x: int, y: int, z: int):
        self.pos = [x, y, z]
        self.vel = [0, 0, 0]

    def __repr__(self):
        return "(%s) => (%s)" % (", ".join(str(c) for c in self.pos), ", ".join(str(c) for c in self.vel))

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]

    @property
    def z(self) -> int:
        return self.pos[2]

    @property
    def xv(self) -> int:
        return self.vel[0]

    @property
    def yv(self) -> int:
        return self.vel[1]

    @property
    def zv(self) -> int:
        return self.vel[2]

    def move(self):
        for i in range(3):
            self.pos[i] += self.vel[i]

    def potential_energy(self) -> int:
        return sum(abs(c) for c in self.pos)

    def kinetic_energy(self) -> int:
        return sum(abs(c) for c in self.vel)

    def total_energy(self) -> int:
        return self.potential_energy() * self.kinetic_energy()

    @staticmethod
    def gravitate(m1: Moon, m2: Moon):
        for i in range(3):
            direction = 1 if m1.pos[i] < m2.pos[i] else 0 if m1.pos[i] == m2.pos[i] else -1
            m1.vel[i] += direction
            m2.vel[i] -= direction


#


#


if __name__ == "__main__":
    main()
