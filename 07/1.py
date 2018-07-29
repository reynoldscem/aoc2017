from argparse import ArgumentParser
import copy


class Program():
    def __init__(self, name, weight, holding):
        self.name = name
        self.weight = weight
        self.holding = copy.deepcopy(holding)
        self.is_carrying = len(self.holding) >= 1

    def __str__(self):
        holding_str = ', '.join(self.holding)
        print('{} ({}) -> {}'.format(self.name, self.weight, holding_str))


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def parse_entry(line):
    import re

    line = re.sub('[()\->,]', '', line)
    element_id, weight_string, *rest = line.split()
    weight = int(weight_string)

    return Program(element_id, weight, rest)
def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    entries = [parse_entry(line) for line in data]
    candidates = {}
    blacklist = set()

    for entry in entries:
        for held_disk_id in entry.holding:
            blacklist.add(held_disk_id)
            candidates.pop(held_disk_id, None)
        if entry.is_carrying and entry.name not in blacklist:
            candidates[entry.name] = entry

    print(list(candidates)[0])


if __name__ == '__main__':
    main()
