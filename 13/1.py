from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def parse_line(line):
    import re
    depth, _range = map(int, re.findall('\d+', line))
    return (depth, _range)


class Layer():
    def __init__(self, depth, range_=0):
        self.depth = depth
        self.range = range_

    def __str__(self):
        line_0 = ' ' + '[' * self.range
        line_1 = '{}'.format(self.depth) + ' ' * self.range
        line_2 = ' ' + ']' * self.range

        if self.range == 0:
            line_0 += '.'
            line_1 += '.'
            line_2 += '.'

        lines = [list(line_0), list(line_1), list(line_2)]
        lines = [
            ''.join(new_line)
            for new_line in zip(*lines)
        ]
        return '\n'.join(lines)

    def __eq__(self, other):
        return self.depth == other.depth

    def __lt__(self, other):
        return self.depth < other.depth

    @staticmethod
    def merge_layer_strings(layer_1, layer_2, fill_char=' '):
        '''Note... layer *could* be a string repr of a layer, or a layer.'''
        from itertools import zip_longest

        fill_count = 3
        if isinstance(layer_1, str):
            if len(layer_1.splitlines()) <= layer_2.range:
                import re
                fill_count = re.match('.*', layer_1).end()

        fill = fill_char * fill_count

        iterator = zip_longest(
            str(layer_1).splitlines(),
            str(layer_2).splitlines(),
            fillvalue=fill
        )
        new_list = [
            '{} {}'.format(first, second)
            for first, second in iterator
        ]
        return '\n'.join(new_list)


class Firewall():
    def __init__(self, layers):
        from copy import deepcopy

        self.layers = deepcopy(layers)
        depths = [layer.depth for layer in self.layers]
        unused_indices = set(range(0, max(depths))) - set(depths)
        for unused_index in unused_indices:
            self.layers.append(Layer(unused_index))

    def __str__(self):
        from functools import reduce
        return reduce(Layer.merge_layer_strings, sorted(self.layers))

def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()
    layers = [Layer(*parse_line(line)) for line in data]
    firewall = Firewall(layers)

    print(firewall)


if __name__ == '__main__':
    main()
