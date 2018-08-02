from argparse import ArgumentParser
from collections import defaultdict


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def parse_line(line):
    import re
    return list(map(int, re.findall('\d+', line)))


class Node:
    nodes_lookup = None

    @classmethod
    def set_lookup(cls, lookup):
        cls.nodes_lookup = lookup

    def __init__(self, index):
        if self.nodes_lookup is None:
            raise ValueError('Must provide lookup table')

        self.index = index
        self.links = {}

    def add_links(self, *node_indices):
        self.links.update(
            {index: self.nodes_lookup[index] for index in node_indices}
        )
        # Back links
        for node_index in node_indices:
            self.nodes_lookup[node_index].links[self.index] = self

    def __repr__(self):
        base_string = '{}'.format(self.index)

        if len(self.links) == 0:
            return base_string
        else:
            return base_string + ' <-> ' + ', '.join(
                map(str, sorted(self.links.keys()))
            )

    def __hash__(self):
        return self.index

    def __eq__(self, other):
        return self.index == other.index

    def __lt__(self, other):
        return self.index < other.index


# https://stackoverflow.com/questions/2912231/
# is-there-a-clever-way-to-pass-the-key-to-defaultdicts-default-factory
class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class Graph:
    def __init__(self):
        self.nodes = keydefaultdict(Node)
        Node.set_lookup(self.nodes)

    def __repr__(self):
        return '\n'.join(
            entry.__repr__() for entry in sorted(self.nodes.values())
        )


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()
    data = [parse_line(line) for line in data]
    graph = Graph()

    for entry in data:
        graph.nodes[entry[0]].add_links(*entry[1:])

    to_visit = [graph.nodes[0]]
    visited = set()
    from itertools import count

    for index in count(1):
        while len(to_visit) > 0:
            visiting = to_visit.pop()
            visited.add(visiting)
            for node in visiting.links.values():
                if node not in visited:
                    to_visit.append(node)
        try:
            to_visit.append((set(graph.nodes.values()) - visited).pop())
        except KeyError:
            print(index)
            import sys
            sys.exit()


if __name__ == '__main__':
    main()
