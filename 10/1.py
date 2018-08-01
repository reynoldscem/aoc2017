from argparse import ArgumentParser

LIST_LEN = 256


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().strip()
    data = list(map(int, data.split(',')))
    print(data)

    circular_list = list(range(LIST_LEN))

    from itertools import cycle, islice
    current_position = 0
    skip = 0
    for length in data:
        circular_iter_with_indices = cycle(enumerate(circular_list))
        if length > 0:
            indices, sublist = zip(*islice(
                circular_iter_with_indices, current_position,
                current_position + length
            ))
            for index, replacement in zip(indices, reversed(sublist)):
                circular_list[index] = replacement
        current_position += length + skip
        skip += 1
    print(circular_list[0] * circular_list[1])


if __name__ == '__main__':
    main()
