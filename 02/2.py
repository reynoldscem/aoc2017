from argparse import ArgumentParser
from itertools import combinations


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        lines = fd.read().splitlines()

    accum = 0
    for line in lines:
        line_numbers = map(int, line.split())
        pairs = map(sorted, combinations(line_numbers, 2))
        for smaller, larger in pairs:
            if larger % smaller == 0:
                accum += larger // smaller
                break

    print(accum)


if __name__ == '__main__':
    main()
