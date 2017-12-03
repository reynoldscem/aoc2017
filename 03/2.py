from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def tuple_add(first, second):
    return first[0] + second[0], first[1] + second[1]


def main():
    number = 325489

    from itertools import cycle
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbours = directions + [
        (1, 1), (-1, -1), (-1, 1), (1, -1)
    ]
    directions = cycle(directions)

    starting_position = (0, 0)
    current_position = starting_position

    values = {starting_position: 1}

    level = 1
    index = 1
    direction = next(directions)
    while True:
        for _ in range(2):
            for _ in range(level):
                current_position = (
                    current_position[0] + direction[0],
                    current_position[1] + direction[1]
                )
                index += 1
                this_cell_value = 0
                for neighbour in neighbours:
                    neighbour_pos = tuple_add(current_position, neighbour)
                    if neighbour_pos in values.keys():
                        this_cell_value += values[neighbour_pos]
                values[current_position] = this_cell_value

                if this_cell_value > number:
                    break
            if this_cell_value > number:
                break
            direction = next(directions)
        if this_cell_value > number:
            break

        level += 1

    print(this_cell_value)


if __name__ == '__main__':
    main()
