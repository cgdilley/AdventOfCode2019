from shared.Intcode import Computer

import pygame
import sys
import time
import random
from typing import List, Tuple, Dict, Optional, Union


def main():
    computer = load()

    # Insert quarters
    computer.registers[0] = 2

    screen, score = play_game(computer, bounds=(41, 23), render_speed=-5, max_screen_size=(1920, 1080))

    print("Final score = %d" % score)


#


def load() -> Computer:
    with open("input/input13.txt", "r") as f:
        return Computer.from_string(f.read())


#


def play_game(computer: Computer, bounds: Tuple[int, int], render_speed: Optional[int] = None,
              max_screen_size: Tuple[int, int] = (1920, 1080)) \
        -> Tuple[Dict[Tuple[int, int], int], int]:
    """
    Plays the game.

    @param computer: The Intcode computer to run
    @param bounds: The bounds of the playing field
    @param render_speed: How quickly to render the game.
        render_speed == None  ::  Do not render at all
        render_speed == 0     ::  Render frame by frame, waiting for mouse clicks to advance to next frame
        render_speed == 1     ::  Render every frame
        render_speed > 1      ::  Render every n frames (n = render_speed), don't render frames in between
        render_speed < 0      ::  Render every frame, pause n milliseconds between each frame (n = -render_speed)
    @param max_screen_size: Tuple of the maximum width and height of the render screen.  Guarantees that at
    either the width or the height will exactly match its corresponding maximum, and the other dimension will
    be less than or equal to its corresponding maximum
    """

    screen, scale = build_game_screen(bounds, max_width=max_screen_size[0], max_height=max_screen_size[1]) \
        if render_speed is not None else (None, 1)

    # Set a function to call whenever input is required to give joystick inputs
    computer.input_method = ai

    screen_info = dict()
    score = 0
    initial_render_complete = False
    steps = 0
    while True:
        steps += 1
        # Get set of outputs
        outputs = computer.run_until_outputs(3)
        # If program halted, quit
        if outputs is None:
            break

        # Check if this is a score output
        if outputs[0] == -1 and outputs[1] == 0:
            score = outputs[2]
            print(score)
        else:
            # Otherwise treat it as rendering output
            screen_info[(outputs[0], outputs[1])] = outputs[2]

            # When the last wall square is done, the entire initial grid has been rendered
            if (outputs[0], outputs[1]) == bounds:
                initial_render_complete = True
                if render_speed is not None:
                    render(screen, screen_info, None, scale, False)

            # If we're rendering to screen, wait until initial render is complete, and then follow rules set by
            # the render speed
            if render_speed is not None and initial_render_complete:
                if outputs[2] == 0:
                    render(screen, screen_info, (outputs[0], outputs[1]), scale, pause_for_clicks=False, flip=False)
                elif render_speed <= 0 or render_speed <= steps:
                    render(screen, screen_info, (outputs[0], outputs[1]), scale,
                           pause_for_clicks=render_speed == 0 and initial_render_complete)
                    steps = 0

                    # If the render speed is less than zero, pause the program for an amount of
                    # milliseconds = the absolute value of that render speed
                    if render_speed < 0:
                        time.sleep(-render_speed / 1000)
    return screen_info, score


def ai(computer: Computer):
    # Give input that would move the player paddle towards the ball
    player_x = computer.registers[392]
    ball_x = computer.registers[388]
    if player_x < ball_x:
        return 1
    elif player_x > ball_x:
        return -1
    else:
        return 0


#


#


def build_game_screen(bounds: Tuple[int, int], max_width: int = 1920, max_height: int = 1080) \
        -> Tuple[pygame.Surface, float]:
    pygame.init()
    scale_x = max_width / bounds[0]
    scale_y = max_height / bounds[1]
    if scale_x < scale_y:
        scale = scale_x
    else:
        scale = scale_y
    width = int(bounds[0] * scale)
    height = int(bounds[1] * scale)

    return pygame.display.set_mode((width, height), pygame.RESIZABLE), scale


#


def render(screen: pygame.Surface, screen_info: Dict[Tuple[int, int], int],
           pos: Optional[Tuple[int, int]],
           scale: float, pause_for_clicks: bool,
           flip: bool = True):
    """
    Renders all asteroids, and draws a laser from the source to the last destroyed asteroid.

    @param screen: The screen surface to draw on
    @param screen_info Information about what to render onto the screen
    @param pos: The specific coordinates to render, rather than render the whole screen.  If given None, renders
    the whole screen.
    @param scale: The drawing scale
    @param pause_for_clicks: Whether or not the game should wait on mouse clicking input before continuing after
    having rendered the asteroids.
    @param flip Whether or not to flip after rendering.  Will not pause if not flipping
    """
    if screen is None:
        return

    block_colors = [(255, 128, 0), (0, 255, 0), (0, 255, 255), (255, 255, 0), (0, 128, 255), (0, 0, 255)]

    items = [(pos, screen_info[pos])] if pos is not None else screen_info.items()

    # Iterate through all asteroids and render them
    for pos, tile in items:
        width = 0
        block_scale = scale
        if tile == 0:
            color = (0, 0, 0)
        elif tile == 1:
            color = (255, 255, 255)
        elif tile == 2:
            color = random.choice(block_colors)
            block_scale *= 0.9
        elif tile == 3:
            color = (255, 50, 50)
        elif tile == 4:
            color = (255, 255, 255)
            block_scale *= 0.6
            width = 2
        else:
            raise Exception("Invalid tile")
        pygame.draw.rect(screen, color, render_rect(pos, scale, block_scale), width)

    if flip:
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
    return


#


def render_pos(coord: Tuple[int, int], scale: float) -> Tuple[int, int]:
    return int(coord[0] * scale), int(coord[1] * scale)


def render_rect(coord: Tuple[int, int], scale: float, square_scale: float) -> pygame.Rect:
    center = render_pos(coord, scale)
    return pygame.Rect(center[0] - int(square_scale / 2), center[1] - int(square_scale / 2), square_scale, square_scale)


#


#


#


if __name__ == "__main__":
    main()
