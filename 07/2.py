from argparse import ArgumentParser
from collections import Counter
import copy


class Program():
    def __init__(self, name, weight, holding, programs_dict=None):
        assert isinstance(programs_dict, dict)

        self.name = name
        self.weight = weight
        self.holding = copy.deepcopy(holding)
        self.is_carrying = len(self.holding) >= 1
        self.programs_dict = programs_dict

        # Add reference for other programs.
        self.programs_dict[name] = self

    def __str__(self):
        holding_str = ', '.join(self.holding)
        return '{} ({})'.format(self.name, self.weight) + (
            ' -> {} ({})'.format(
                holding_str, self.get_tower_weight()
            ) if self.is_carrying else ''
        )

    __repr__ = __str__

    def children(self):
        return (
            self.programs_dict[child_string]
            for child_string in self.holding
        )

    def children_weights(self):
        return (
            child.get_tower_weight()
            for child in self.children()
        )

    def children_balanced(self):
        weights = list(self.children_weights())
        return len(set(weights)) == 1

    def get_tower_weight(self):
        tower_weight = self.weight + sum(self.children_weights())
        # print(self)
        return tower_weight


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def parse_entry(line, programs_dict):
    import re

    line = re.sub('[()\->,]', '', line)
    element_id, weight_string, *rest = line.split()
    weight = int(weight_string)

    return Program(element_id, weight, rest, programs_dict)


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    # To share state.
    programs_dict = {}
    entries = [parse_entry(line, programs_dict) for line in data]
    candidates = {}
    blacklist = set()

    for entry in entries:
        for held_disk_id in entry.holding:
            blacklist.add(held_disk_id)
            candidates.pop(held_disk_id, None)
        if entry.is_carrying and entry.name not in blacklist:
            candidates[entry.name] = entry

    top_entry_name = list(candidates.keys())[0]
    top_entry = list(candidates.values())[0]
    print(top_entry_name)
    print(top_entry.get_tower_weight())
    print()

    del candidates, blacklist, entries, data

    candidates = []
    candidates.append(top_entry)
    while True:
        candidate = candidates.pop()
        children_balanced = candidate.children_balanced()
        if not children_balanced:
            # Note, overwriting is possible. Since
            weight_to_program_map = {
                child.get_tower_weight(): child
                for child in candidate.children()
            }
            weight_frequencies = Counter(
                candidate.children_weights()
            ).most_common()
            odd_weight_out = weight_frequencies[-1][0]
            modal_weight = weight_frequencies[0][0]

            odd_child = weight_to_program_map[odd_weight_out]
            if odd_child.children_balanced():
                print(odd_child.name)
                print(list(odd_child.children_weights()))
                print(odd_child.weight + (modal_weight - odd_weight_out))
                break
            else:
                for child in odd_child.children():
                    candidates.append(child)


if __name__ == '__main__':
    main()
