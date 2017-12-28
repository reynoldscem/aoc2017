from argparse import ArgumentParser
from itertools import islice


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def make_generator(seed_value, factor, multiplier):
    modulo_val = 2**31 - 1
    value = seed_value
    while True:
        value *= factor
        value %= modulo_val
        if value % multiplier == 0:
            yield '{0:016b}'.format(value)[-16:]


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()
    generator_a_seed = int(data[0].split()[-1])
    generator_b_seed = int(data[1].split()[-1])
    generator_a = make_generator(generator_a_seed, 16807, 4)
    generator_b = make_generator(generator_b_seed, 48271, 8)

    combined_generator = zip(generator_a, generator_b)

    equal_generator = (a == b for a, b in combined_generator)
    truncated_generator = islice(equal_generator, 5 * 10**6)

    matching_count = sum(truncated_generator)

    print(matching_count)


if __name__ == '__main__':
    main()
