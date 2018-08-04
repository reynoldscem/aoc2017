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

        if self.range >= 1:
            self.scanner_position = 0
        else:
            self.scanner_position = None

        self.has_packet = False
        self.severity = 0
        self.direction = 1

    def __str__(self):
        line_0 = ' ' + '[' * self.range

        # Print depth modulo 10 to keep width at 1 char.
        line_1 = '{}'.format(self.depth % 10) + ' ' * self.range
        line_2 = ' ' + ']' * self.range

        if self.range == 0:
            line_0 += '.'
            line_1 += '.'
            line_2 += '.'
        else:
            line_1_list = list(line_1)
            line_1_list[self.scanner_position + 1] = 'S'

            # Doesn't matter that it's a list now.
            line_1 = line_1_list

        if self.has_packet:
            line_0_list = list(line_0)
            line_0_list[1] = '('
            line_0 = line_0_list

            line_2_list = list(line_2)
            line_2_list[1] = ')'
            line_2 = line_2_list

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

    def tick(self):
        if self.range >= 1:
            self.scanner_position = (self.scanner_position + self.direction)
            if self.scanner_position == self.range - 1 or self.scanner_position == 0:
                self.direction *= -1

    def packet_enter(self):
        self.has_packet = True
        if self.scanner_position == 0:
            self.severity = self.depth * self.range

            return self.severity
        else:
            return 0

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
        self.layers = sorted(self.layers)

        self.packet_position = -1
        self.severity = 0

    def tick(self):
        self.layers[self.packet_position].has_packet = False
        self.packet_position += 1
        try:
            self.severity += self.layers[self.packet_position].packet_enter()
        except:
            raise IndexError('Packet has left')

        for layer in self.layers:
            layer.tick()

    def __str__(self):
        from functools import reduce
        return reduce(Layer.merge_layer_strings, self.layers)

def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()
    layers = [Layer(*parse_line(line)) for line in data]

    firewall = Firewall(layers)
    print('Initial state')
    print(firewall)
    from itertools import count
    for picosecond in count():
        try:
            firewall.tick()
        except IndexError:
            print()
            print('Trip cost: {}'.format(firewall.severity))
            print()
            break
        print('Picosecond {}'.format(picosecond))
        print(firewall)

    print('Final state')
    print(firewall)


if __name__ == '__main__':
    main()
