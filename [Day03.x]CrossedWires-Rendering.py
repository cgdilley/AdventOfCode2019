import pygame
from shared.day3 import load_wires, Wire
import time
import sys


from typing import Tuple
Coord = Tuple[int, int]


def main():
    wire1, wire2 = load_wires()

    render_wires(wire1, wire2, progressive=True, speed=20)


#


#


def render_wires(*wires: Wire, progressive: bool, speed: int):
    bounds = ((
                  min([c[0] for w in wires for c in w.coords]),
                  min([c[1] for w in wires for c in w.coords])
              ),
              (
                  max([c[0] for w in wires for c in w.coords]),
                  max([c[1] for w in wires for c in w.coords])
              ))

    # Calculate window size based on bounds, and determine scale factor
    pygame.init()
    max_width, max_height = 1920, 1080
    width, height = bounds[1][0] - bounds[0][0], bounds[1][1] - bounds[0][1]
    scale_x = 1 if width < max_width else max_width / width
    scale_y = 1 if height < max_height else max_height / height
    if scale_x < scale_y:
        scale = scale_x
        width = int(width * scale_x)
        height = int(width * scale_x)
    else:
        scale = scale_y
        width = int(width * scale_y)
        height = int(height * scale_y)

    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # Keep track of coords traversed
    seen = set()
    seen_by_index = {i: set() for i in range(len(wires))}
    red_render_coords = set()

    max_steps = max([w.total_length for w in wires])

    for step in range(max_steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Render each wire
        for i, w in enumerate(wires):
            if step >= len(w.raw):
                continue
            c = w.raw[step]
            render_c = _offset(c, bounds=bounds, scale=scale)
            if c in seen and c not in seen_by_index[i]:
                color = (255, 0, 0)
                size = 5
                for x in range(render_c[0] - int(size/2), render_c[0] + int(size/2)):
                    for y in range(render_c[1] - int(size/2), render_c[1] + int(size/2)):
                        red_render_coords.add((x, y))
            elif c in seen:
                color = (255, 0, 0)
                size = 1
                red_render_coords.add(render_c)
            elif render_c in red_render_coords:
                color = (255, 0, 0)
                size = 1
            else:
                color = _wire_color(i)
                size = 1
            pygame.draw.rect(screen,
                             color,
                             pygame.Rect(render_c[0] - int(size/2), render_c[1] - int(size/2), size, size))
            seen.add(c)
            seen_by_index[i].add(c)

        if progressive and step % speed == 0:
            pygame.display.flip()
            # time.sleep(0.0001)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

#


def _offset(coord: Coord, bounds: Tuple[Coord, Coord], scale: float) -> Coord:
    return (int((coord[0] - bounds[0][0]) * scale),
            int((coord[1] - bounds[0][1]) * scale))


def _wire_color(index: int) -> Tuple[int, int, int]:
    if index == 0:
        return 150, 150, 230
    elif index == 1:
        return 150, 230, 150
    else:
        return 255, 255, 255


#


if __name__ == "__main__":
    main()
