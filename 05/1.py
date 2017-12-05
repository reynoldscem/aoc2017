from argparse import ArgumentParser
from itertools import count


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    jumps = [int(entry) for entry in data]

    index = 0
    for steps in count(1):
        next_index = index + jumps[index]

        jumps[index] += 1
        index = next_index

        if index < 0 or index >= len(jumps):
            break

    print(steps)


if __name__ == '__main__':
    main()
