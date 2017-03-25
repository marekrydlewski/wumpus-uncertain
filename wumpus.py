import sys
import numpy as np
from collections import defaultdict


def set_neighbors(arr, coords, value=-1):
    i, j = coords
    y, x = arr.shape

    if i - 1 >= 0:
        arr[i - 1][j] = value
    if i + 1 < x:
        arr[i + 1][j] = value
    if j - 1 >= 0:
        arr[i][j - 1] = value
    if j + 1 < y:
        arr[i][j + 1] = value


def set_neighbors_except(arr, coords, value, no_set=-1):
    i, j = coords
    y, x = arr.shape
    neighbors = list()

    if i - 1 >= 0 and arr[i - 1][j] != no_set:
        arr[i - 1][j] = value
        neighbors.append((i - 1, j))
    if j - 1 >= 0 and arr[i][j - 1] != no_set:
        arr[i][j - 1] = value
        neighbors.append((i, j - 1))
    if j + 1 < y and arr[i][j + 1] != no_set:
        arr[i][j + 1] = value
        neighbors.append((i, j + 1))
    if i + 1 < x and arr[i + 1][j] != no_set:
        arr[i + 1][j] = value
        neighbors.append((i + 1, j))

    return neighbors


def get_max_neighbor(arr, coords):
    i, j = coords
    y, x = arr.shape

    max_value = -1
    if i - 1 >= 0:
        if arr[i - 1][j] > max_value:
            max_value = arr[i - 1][j]
    if i + 1 < x:
        if arr[i + 1][j] > max_value:
            max_value = arr[i + 1][j]
    if j - 1 >= 0:
        if arr[i][j - 1] > max_value:
            max_value = arr[i][j - 1]
    if j + 1 < y:
        if arr[i][j + 1] > max_value:
            max_value = arr[i][j + 1]
    return max_value


def get_neighbors_pos(pos):
    i, j = pos
    return [(i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1)]


def get_combinations(size):
    height = 2 ** size
    output = np.zeros((height, size), dtype=bool)
    jump = 2 ** size / 2

    for x in range(size):
        i = 0
        to_set = True
        for y in range(height):
            if to_set:
                output[y][x] = True
            i += 1
            if (i == jump):
                to_set = not to_set
                i = 0
        jump /= 2
    return output


def get_possible_areas(data):
    y, x = data.shape
    possible = np.zeros((y, x), dtype=int)

    for i in range(x):
        for j in range(y):
            if data[i][j] == 'O':
                possible[i][j] = -1
                set_neighbors(possible, (i, j), -1)
            elif data[i][j] == 'B':
                possible[i][j] = -1

    return possible


def get_breeze_checked(breeze, traps, front):
    breeze_checked = {b: False for b in breeze}
    for i in range(len(traps)):
        if traps[i] == True:
            neigh = get_neighbors_pos(front[i])
            for n in neigh:
                if n in breeze_checked:
                    breeze_checked[n] = True
    return breeze_checked


def get_fronts(data):
    y, x = data.shape
    curr_max = 0
    fronts = get_possible_areas(data)
    breeze_in_fronts = np.zeros((y, x), dtype=int)
    breeze_indexes = defaultdict(list)
    front_indexes = defaultdict(list)

    for i in range(x):
        for j in range(y):
            if data[i][j] == 'B':
                max_neigbor = get_max_neighbor(fronts, (i, j))
                if max_neigbor <= 0:
                    curr_max += 1
                    neighbors = set_neighbors_except(fronts, (i, j), curr_max, -1)
                    breeze_in_fronts[i][j] = curr_max

                    front_indexes[curr_max].extend(neighbors)
                    breeze_indexes[curr_max].append((i, j))
                else:
                    neighbors = set_neighbors_except(fronts, (i, j), max_neigbor, -1)
                    breeze_in_fronts[i][j] = max_neigbor

                    front_indexes[max_neigbor].extend(neighbors)
                    breeze_indexes[max_neigbor].append((i, j))

    return fronts, breeze_in_fronts, front_indexes, breeze_indexes


def wumpus():
    """
    fronts = table with fronts, 0 nothing (normal probability), -1 no front coz O in sensor, >= 1 fronts
    """
    with open(sys.argv[1], "r") as input_f:
        input = input_f.readlines()
    n, m = map(int, input[0].strip().split(' '))
    prob_hole = float(input[1])
    data = np.array([list(line.strip()) for line in input[2:(2 + n)]])

    fronts, breezes, front_indexes, breeze_indexes = get_fronts(data)
    print(fronts)
    print(front_indexes)
    print()
    print(breezes)
    print()
    print(breeze_indexes)

    for k, front in front_indexes.items():
        breeze = breeze_indexes[k]
        trap_table = get_combinations(len(front))
        #print(front, "breeze:", breeze)
        for traps in trap_table:  # check one variant of trap setting
            breeze_checked = get_breeze_checked(breeze, traps, front)
            #print(breeze_checked, traps)

    output = np.zeros((n, m), dtype=float)
    with open(sys.argv[2], "w+") as output_f:
        pass
    return


def main():
    if len(sys.argv) < 3 or sys.argv[0] == '-h':
        print("Pass proper args")
        exit(0)
    wumpus()


if __name__ == '__main__':
    main()
