from argparse import ArgumentParser


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
        line_numbers = list(map(int, line.split()))
        line_min, line_max = min(line_numbers), max(line_numbers)
        line_diff = line_max - line_min

        accum += line_diff

    print(accum)


if __name__ == '__main__':
    main()
