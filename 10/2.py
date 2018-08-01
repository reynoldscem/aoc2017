from argparse import ArgumentParser
from itertools import cycle, islice
from functools import reduce
import operator

LIST_LEN = 256
MAGIC_SUFFIX = [17, 31, 73, 47, 23]


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


# https://stackoverflow.com/questions/312443/
#  how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().strip()
    data = list(map(ord, data)) + MAGIC_SUFFIX

    circular_list = list(range(LIST_LEN))

    current_position = 0
    skip = 0
    for _round in range(64):
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

    out_data = []
    for chunk in chunks(circular_list, 16):
        out_value = reduce(operator.xor, chunk)
        out_data.append(format(out_value, 'x'))
    print(''.join(out_data))


if __name__ == '__main__':
    main()
