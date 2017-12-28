from itertools import count, islice, chain, cycle
from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    parser.add_argument('--debug', action='store_true', default=False)

    return parser


def get_index_iterator(index_of_bank, num_banks, num_blocks):
    # Get an iterator for the next bank until the end of list index,
    #  then get a cycling iterator for all banks. Join them,
    #  and take the correct number of its before throwing a
    #  StopIteration.
    first_cycle = range(index_of_bank + 1, num_banks)
    index_cycles = cycle(range(num_banks))

    index_iterator = chain(first_cycle, index_cycles)

    return islice(index_iterator, num_blocks)


def main():
    args = build_parser().parse_args()

    # Just assume filename is legit, and format
    #  is correct.
    with open(args.filename) as fd:
        data = fd.read().strip().split()

    # Need to modify values / use .index.
    # So construct a list.
    banks = list(map(int, data))

    # To track if we're in a cycle.
    states = set()

    for cycle_index in count(1):
        # Luckily ties are broken by the lowest index,
        #  which matches python's behaviour.
        # Grab the bank with highest value, record that value,
        #  and zero that bank out.
        max_value = max(banks)
        max_index = banks.index(max_value)
        banks[max_index] = 0

        if args.debug:
            print(
                '{} has most blocks with {}'
                ''.format(max_index + 1, max_value)
            )

        # Given the current info get an iterator for where
        #  to deposit blocks. Walk over it increment.
        index_iterator = get_index_iterator(max_index, len(banks), max_value)
        for distribution_index in index_iterator:
            banks[distribution_index] += 1

        # Make state hashable by constructing a tuple.
        #  Check if it's in our visited set, if it is break,
        #  if not add it in.
        frozen_state = tuple(banks)
        if frozen_state in states:
            break
        states.add(frozen_state)

    print(cycle_index)


if __name__ == '__main__':
    main()
