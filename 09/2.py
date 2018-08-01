from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def prune_nots(data):
    trap = True
    while trap:
        for index, entry in enumerate(data):
            if entry == '!':
                data = data[:index] + data[index+2:]
                break
            if index == len(data) - 1:
                trap = False
    return data


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()
    entries = data
    for data in entries:
        data = list(data)
        data = prune_nots(data)

        groups = 0
        score = 0
        group_depth = 0
        max_group_depth = 0
        garbage_chars = 0
        garbage_mode = False
        for character in data:
            if garbage_mode:
                if character == '>':
                    garbage_mode = False
                else:
                    garbage_chars += 1
            else:
                if character == '{':
                    group_depth += 1
                    groups += 1
                    score += group_depth
                    max_group_depth = max(max_group_depth, group_depth)
                elif character == '}':
                    group_depth -= 1
                elif character == '<':
                    garbage_mode = True
        assert group_depth == 0
        print(max_group_depth)
        print(groups)
        print(score)
        print(garbage_chars)
        print()


if __name__ == '__main__':
    main()
