from typing import List


def main():
    image = load(width=25, height=6)

    merged = merge_layers(image, width=25, height=6, layers=len(image))

    print(render_image(merged))


def load(width: int, height: int) -> List[List[List[int]]]:
    with open("input/input08.txt", "r") as f:
        digits = [int(d) for d in f.read().strip()]
    pixels_per_layer = width * height
    return [[[
        digits[(layer * pixels_per_layer) + (row * width) + column]
        for column in range(width)
    ] for row in range(height)
    ] for layer in range(int(len(digits) / pixels_per_layer))]


def merge_layers(image: List[List[List[int]]], width: int, height: int, layers: int) -> List[List[int]]:
    merged = [[2 for c in range(width)] for r in range(height)]
    for row in range(height):
        for col in range(width):
            for layer in range(layers):
                if image[layer][row][col] != 2:
                    merged[row][col] = image[layer][row][col]
                    break
    return merged


def render_image(image: List[List[int]]) -> str:
    pixels = {
        0: " ",
        1: "O",
        2: "-"
    }
    return "\n".join([
        " ".join([pixels[image[row][col]] for col in range(len(image[row]))])
        for row in range(len(image))])


if __name__ == "__main__":
    main()
