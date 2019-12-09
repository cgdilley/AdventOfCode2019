from shared.Intcode import Computer


def main():
    computer = load()

    outputs = computer.run()

    print(outputs)


def load() -> Computer:
    with open("input/input09.txt", "r") as f:
        return Computer.from_string(f.read(), inputs=[1])


if __name__ == "__main__":
    main()
