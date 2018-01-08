from argparse import ArgumentParser
import copy


class Program():
    def __init__(self, name, weight, holding):
        self.name = name
        self.weight = weight
        self.holding = copy.deepcopy(holding)


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()
    data


if __name__ == '__main__':
    main()
