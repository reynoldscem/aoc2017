from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def main():
    number = 325489
    from itertools import cycle
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    directions = cycle(directions)

    starting_position = (0, 0)
    current_position = starting_position

    level = 1
    index = 1
    direction = next(directions)
    while index < number:
        for _ in range(2):
            for _ in range(level):
                current_position = (
                    current_position[0] + direction[0],
                    current_position[1] + direction[1]
                )
                index += 1
                if index == number:
                    break
            if index == number:
                break
            direction = next(directions)

        level += 1

    print(abs(current_position[0]) + abs(current_position[1]))


if __name__ == '__main__':
    main()
