from argparse import ArgumentParser
import operator
import re


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def parse_instruction(raw_instruction):
    instruction_regex = re.compile(
        '^([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) (!=|>|>=|<|<=|==) (-?\d+)$'
    )
    token_LUT = {
        'inc': operator.
    }
    (
        register_name, operator_token, operand, compar_1, comparator, compar_2
    ) = re.match(instruction_regex).groups()

    operand = int(operand)
    compar_2 = int(compar_2)

    operator = token_LUT[operator_token]


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().strip()

    accum = 0
    data_wrapped = data + data[0]
    for index in range(len(data_wrapped) - 1):
        first_char, second_char = data_wrapped[index:index + 2]
        if first_char == second_char:
            accum += int(first_char)
    print(accum)


if __name__ == '__main__':
    main()
