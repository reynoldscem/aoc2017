from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    parser.add_argument('--debug', action='store_true', default=False)

    return parser


def update_position(position, update):
    return tuple(
        first + second
        for first, second in zip(position, update)
    )


def distance_from_origin(position):
    return max(map(abs, position))


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().strip()

    directions = data.split(',')

    coordinate_lookup = {
        'se': (1, -1, 0), 'ne': (1, 0, -1), 'n': (0, 1, -1),
        'nw': (-1, 1, 0), 'sw': (-1, 0, +1), 's': (0, -1, +1)
    }

    position = (0, 0, 0)

    if args.debug:
        print(position)
        print()

    max_dist = 0
    for direction in directions:
        direction_vector = coordinate_lookup[direction]
        position = update_position(position, direction_vector)

        distance = distance_from_origin(position)
        max_dist = max(max_dist, distance)

        if args.debug:
            print(position)
            print()

    print(max_dist)


if __name__ == '__main__':
    main()
