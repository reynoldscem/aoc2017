from argparse import ArgumentParser
from itertools import permutations


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('filename')

    return parser


def anagrams_of_string(string):
    return set(
        ''.join(entry)
        for entry in permutations(string, len(string))
    )


def valid_pass(passphrase):
    word_list = passphrase.split()
    if len(set(word_list)) != len(word_list):
        return False

    anagrams = set()
    for string in word_list:
        for new_anagram in anagrams_of_string(string):
            if new_anagram in anagrams:
                return False
            else:
                anagrams.add(new_anagram)

    return True


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
