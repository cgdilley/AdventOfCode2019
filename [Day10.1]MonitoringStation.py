from __future__ import annotations
from typing import Dict, Union, Set, Tuple


def main():
    asteroids = load()

    los_count = get_los_count(asteroids)

    a_coord, a_count = max(los_count.items(), key=lambda i: i[1])

    print("The asteroid with the greatest number of visible asteroids is at position %s, "
          "with %d visible asteroids." % (str(a_coord), a_count))
    

def load() -> Set[Coord]:
    with open("input/input10.txt", "r") as f:
        grid = f.readlines()
    asteroids = set()
    for r, row in enumerate(grid):
        for c, col in enumerate(row.strip()):
            if col == "#":
                asteroids.add(Coord(c, r))
    return asteroids


def has_los(a1: Coord, a2: Coord, asteroids: Set[Coord]) -> bool:
    # Handle vertical case special, to avoid division by zero
    if a1.x == a2.x:
        step = 1 if a2.y > a1.y else -1
        for y in range(a1.y + step, a2.y, step):
            if (a1.x, y) in asteroids:
                return False
    else:
        # Calculate slope and y-intercept of line between the asteroids
        slope = (a2.y - a1.y) / (a2.x - a1.x)
        intercept = a1.y - (slope * a1.x)

        # Move along x positions in the line, identifying positions that have integer y values
        # Test whether those x, y coordinates exist in the asteroid set
        step = 1 if a2.x > a1.x else -1
        for x in range(a1.x + step, a2.x, step):
            # y = mx + b, throwback tuesday
            y = (slope * x) + intercept
            rounded = round(y)

            # Account for float error
            if abs(y - rounded) > 0.000001:
                continue
            
            if (x, rounded) in asteroids:
                return False
    return True


def get_los_count(asteroids: Set[Coord]) -> Dict[Coord, int]:
    los_count = {a: 0 for a in asteroids}
    asteroid_list = list(asteroids)

    # Test the line-of-sight of all asteroid pairs
    for i, a1 in enumerate(asteroid_list):
        for a2 in asteroid_list[i+1:]:
            if has_los(a1, a2, asteroids):
                los_count[a1] += 1
                los_count[a2] += 1
    return los_count


class Coord:
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, o: Union[Coord, Tuple[int, int]]):
        if type(o) == tuple:
            return self.x == o[0] and self.y == o[1]
        return self.x == o.x and self.y == o.y

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)


if __name__ == "__main__":
    main()
