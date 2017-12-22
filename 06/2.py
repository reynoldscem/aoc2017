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
    for index in range(len(data)):
        first_char = data[index]
        second_char = data[(index + len(data) // 2) % len(data)]
        if first_char == second_char:
            accum += int(first_char)
    print(accum)


if __name__ == '__main__':
    main()
