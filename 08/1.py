from argparse import ArgumentParser
from collections import defaultdict
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
    function_LUT = {
        'inc': operator.add,
        'dec': operator.sub,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq
    }

    (
        register_name, operator_token, operand,
        compar_1, comparator_token, compar_2
    ) = re.match(instruction_regex, raw_instruction).groups()

    operand = int(operand)
    compar_2 = int(compar_2)

    operator_function = function_LUT[operator_token]
    comparator_function = function_LUT[comparator_token]

    return (
        register_name, operator_function, operand,
        compar_1, comparator_function, compar_2
    )


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()
    instruction_stream = map(parse_instruction, data)

    registers = defaultdict(int)
    for instruction in instruction_stream:
        (
            register_name, operator_function, operand,
            compar_1, comparator_function, compar_2
        ) = instruction
        compar_1_value = registers[compar_1]
        if comparator_function(compar_1_value, compar_2):
            registers[register_name] = operator_function(
                registers[register_name], operand
            )

    print(max(registers.values()))


if __name__ == '__main__':
    main()
