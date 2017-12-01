from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


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
