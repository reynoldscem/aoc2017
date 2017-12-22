from itertools import count, islice, chain, cycle
from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    parser.add_argument('--debug', action='store_true', default=False)

    return parser


def get_index_iterator(index_of_bank, num_banks, num_blocks):
    first_cycle = range(index_of_bank + 1, num_banks)
    index_cycles = cycle(range(num_banks))

    index_iterator = chain(first_cycle, index_cycles)

    return islice(index_iterator, num_blocks)


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().strip().split()

    banks = list(map(int, data))

    states = set()

    for cycle_index in count(1):
        max_value = max(banks)
        max_index = banks.index(max_value)
        banks[max_index] = 0

        if args.debug:
            print(
                '{} has most blocks with {}'
                ''.format(max_index + 1, max_value)
            )

        index_iterator = get_index_iterator(max_index, len(banks), max_value)
        for distribution_index in index_iterator:
            banks[distribution_index] += 1

        frozen_state = tuple(banks)
        if frozen_state in states:
            break
        states.add(frozen_state)

    print(cycle_index)


if __name__ == '__main__':
    main()
