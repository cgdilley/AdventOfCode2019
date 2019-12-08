from typing import List, Dict


def main():
    image = load(width=25, height=6)

    layer_info = count_digits_per_layer(image, width=25, height=6, layers=len(image))

    fewest_zeroes_layer, fewest_zeroes_info = min(layer_info.items(), key=lambda i: i[1][0])
    print("The layer with the fewest 0s is layer %d, with %d 0s.  This layer has %d 1s and %d 2s, which "
          "multiplied together = %d." % (
              fewest_zeroes_layer,
              fewest_zeroes_info[0],
              fewest_zeroes_info[1],
              fewest_zeroes_info[2],
              fewest_zeroes_info[1] * fewest_zeroes_info[2]
          ))


def load(width: int, height: int) -> List[List[List[int]]]:
    with open("input/input08.txt", "r") as f:
        digits = [int(d) for d in f.read().strip()]
    pixels_per_layer = width * height
    return [[[
        digits[(layer * pixels_per_layer) + (row * width) + column]
        for column in range(width)
    ] for row in range(height)
    ] for layer in range(int(len(digits) / pixels_per_layer))]


def count_digits_per_layer(image: List[List[List[int]]], width: int, height: int, layers: int) \
        -> Dict[int, Dict[int, int]]:
    info = {i: dict() for i in range(layers)}
    for layer in range(layers):
        for row in range(height):
            for column in range(width):
                d = image[layer][row][column]
                if d not in info[layer]:
                    info[layer][d] = 1
                else:
                    info[layer][d] += 1
    return info


if __name__ == "__main__":
    main()
