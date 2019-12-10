from __future__ import annotations
from typing import Dict, Union, Set, Tuple, Optional, List, Iterable
import math
import pygame
import sys
import time


def main():
    asteroids = load()

    destroyed = run_laser(source=Coord(17, 22),
                          until_num_destroyed=200,
                          asteroids=asteroids,
                          render_speed=-25)

    print("The 200th destroyed asteroid was: %s" % str(destroyed[-1]))


def load() -> Set[Coord]:
    with open("input/input10.txt", "r") as f:
        grid = f.readlines()
    asteroids = set()
    for r, row in enumerate(grid):
        for c, col in enumerate(row.strip()):
            if col == "#":
                asteroids.add(Coord(c, r))
    return asteroids


def sort_by_angles(source: Coord, asteroids: Set[Coord]) -> Dict[float, List[Coord]]:
    angle_map = dict()
    for asteroid in asteroids:
        if asteroid == source:
            continue
        angle = source.angle_to(asteroid)
        angle = round(angle, 8)
        if angle in angle_map:
            angle_map[angle].append(asteroid)
        else:
            angle_map[angle] = [asteroid]
    return {a: sorted(l, key=lambda c: source.distance_to(c)) for a, l in angle_map.items()}


def run_laser(source: Coord, until_num_destroyed: int, asteroids: Set[Coord],
              render_speed: Optional[int] = None):
    # Copy asteroids list
    angles = sort_by_angles(source, asteroids)

    # Sort the angle map in order of angle, starting vertical and going clockwise
    angles = sorted(angles.items(), key=lambda a: a[0], reverse=True)
    bounds = Coord(max(asteroids, key=lambda c: c.x).x, max(asteroids, key=lambda c: c.y).y)

    destroyed = list()

    screen, scale = build_game_screen(bounds) if render_speed is not None else (None, None)

    # Keep destroying asteroids until quota is met
    while len(destroyed) < until_num_destroyed and len(destroyed) < len(asteroids) - 1:
        for angle, asteroid_list in angles:
            if len(asteroid_list) > 0:
                destroyed.append(asteroid_list.pop(0))
                if render_speed is not None:
                    if render_speed <= 0 or len(destroyed) % render_speed == 0:
                        render_asteroids(screen, asteroids, destroyed, source, bounds, scale,
                                         pause_for_clicks=render_speed == 0)
                    if render_speed < 0:
                        time.sleep(-render_speed / 1000)
                if len(destroyed) == until_num_destroyed:
                    break

    return destroyed

#


#


# RENDERING
#


def build_game_screen(bounds: Coord, max_width: int = 1920, max_height: int = 1080) -> Tuple[pygame, float]:
    pygame.init()
    scale_x = max_width / bounds.x
    scale_y = max_height / bounds.y
    if scale_x < scale_y:
        scale = scale_x
    else:
        scale = scale_y
    width = int(bounds.x * scale)
    height = int(bounds.y * scale)

    return pygame.display.set_mode((width, height), pygame.RESIZABLE), scale

#


def render_asteroids(screen: pygame.Surface, asteroids: Set[Coord], destroyed: List[Coord], source: Coord,
                     bounds: Coord, scale: float, pause_for_clicks: bool):
    """
    Renders all asteroids, and draws a laser from the source to the last destroyed asteroid.

    @param screen: The screen surface to draw on
    @param asteroids: The set of all asteroid coordinates
    @param destroyed: The set of all destroyed asteroid coordinates
    @param source: The source coordinates of the laser
    @param bounds: The maximum X and Y values of the grid space, as a single coordinate
    @param scale: The drawing scale
    @param pause_for_clicks: Whether or not the game should wait on mouse clicking input before continuing after
    having rendered the asteroids.
    """
    if screen is None:
        return

    # Wipe the screen
    screen.fill((0, 0, 0))

    # Get the target asteroid, if any
    target = destroyed[-1] if len(destroyed) > 0 else None

    # Draw laser
    if target is not None:
        pygame.draw.line(screen, (255, 0, 0), render_pos(source, scale), render_pos(target, scale), int(scale / 5))

    # Iterate through all asteroids and render them
    for asteroid in asteroids:
        if asteroid == source:
            color = (0, 0, 255)
        elif asteroid == target:
            color = (255, 128, 0)
        elif asteroid in destroyed:
            color = (100, 100, 100)
        else:
            color = (255, 255, 255)
        pygame.draw.rect(screen, color, render_rect(asteroid, scale, scale / 4))
    pygame.display.flip()

    pause_rendering = True
    while pause_rendering:
        for event in pygame.event.get():
            # End program if window is closed
            if event.type == pygame.QUIT:
                sys.exit()
            # Unpause on click, if pausing for clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pause_rendering = False
        # If not pausing on clicks, just continue
        if not pause_for_clicks:
            pause_rendering = False

#


def render_pos(coord: Coord, scale: float) -> Tuple[int, int]:
    return int(coord.x * scale), int(coord.y * scale)


def render_rect(coord: Coord, scale: float, square_scale: float) -> pygame.Rect:
    center = render_pos(coord, scale)
    return pygame.Rect(center[0] - int(square_scale / 2), center[1] - int(square_scale / 2), square_scale, square_scale)


#


#


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

    def __add__(self, other: Union[Coord, Tuple[int, int]]):
        if type(other) == tuple:
            return Coord(self.x + other[0], self.y + other[1])
        return Coord(self.x + other.x, self.y + other.y)

    def angle_to(self, other: Coord) -> float:
        return math.atan2(other.x - self.x, other.y - self.y)

    def distance_to(self, other: Coord) -> float:
        return (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)) ** 0.5


#


#


if __name__ == "__main__":
    main()
