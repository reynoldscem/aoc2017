from itertools import product
from functools import reduce
import operator

accepted_instructions = {'A', 'B', 'Down', 'Left', 'Right', 'Start', 'Up'}


def tuple_fun(*tuples, fun=sum):
    return tuple(map(fun, zip(*tuples)))


def tuple_add(*tuples):
    return tuple_fun(
        *tuples, fun=sum
    )


def tuple_minus(*tuples):
    return tuple_fun(
        *tuples, fun=lambda x: reduce(operator.__sub__, x)
    )


def minkowski(tuple_1, tuple_2=(0, 0)):
    return sum(map(abs, tuple_minus(tuple_1, tuple_2)))


def main():
    with open('./data/1.txt') as fd:
        instructions = fd.read().strip().split(', ')

    assert set(instructions).issubset(accepted_instructions), (
        'Invalid instructions: {}'
        ''.set(instructions).difference(accepted_instructions)
    )
    assert instructions[-1] == 'Start'

    instructions = instructions[:-1]

    position = (0, 0)
    A_markers = []
    B_markers = []

    for instruction in instructions:
        if instruction == 'Up':
            position = tuple_add(position, (0, 1))
        elif instruction == 'Down':
            position = tuple_add(position, (0, -1))
        elif instruction == 'Left':
            position = tuple_add(position, (-1, 0))
        elif instruction == 'Right':
            position = tuple_add(position, (1, 0))
        elif instruction == 'A':
            A_markers.append(position)
        elif instruction == 'B':
            B_markers.append(position)
        else:
            raise Exception

    # Part 1.
    all_markers = list(set(A_markers + B_markers))
    distances = list(map(minkowski, all_markers))
    max_distance = max(distances)

    # It says to identify the marker...
    max_distance_index = distances.index(max_distance)
    _ = all_markers[max_distance_index]
    _

    print(max_distance)

    # Part 2.
    pairs = product(A_markers, B_markers)
    max_pair = max(map(lambda x: minkowski(*x), pairs))
    print(max_pair)


if __name__ == '__main__':
    main()
