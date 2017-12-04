from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def valid_pass(string):
    word_list = string.split()
    return len(set(word_list)) == len(word_list)


def main():
    args = build_parser().parse_args()
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    valid_passphrases = [
        passphrase
        for passphrase in data
        if valid_pass(passphrase)
    ]
    num_valid = len(valid_passphrases)
    print(num_valid)


if __name__ == '__main__':
    main()
