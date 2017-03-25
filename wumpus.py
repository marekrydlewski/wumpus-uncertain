import sys
import numpy as np


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


def set_neighbors_except(arr, coords, value, no_set = -1):
    i, j = coords
    y, x = arr.shape

    if i - 1 >= 0 and arr[i - 1][j] != no_set:
        arr[i - 1][j] = value
    if i + 1 < x and arr[i + 1][j] != no_set:
        arr[i + 1][j] = value
    if j - 1 >= 0 and arr[i][j - 1] != no_set:
        arr[i][j - 1] = value
    if j + 1 < y and arr[i][j+1] != no_set:
        arr[i][j + 1] = value


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


def get_fronts(data):
    y, x = data.shape
    #fronts = np.zeros((y, x), dtype=int)

    fronts = get_possible_areas(data)
    print(fronts)
    curr_max = 0
    for i in range(x):
        for j in range(y):
            if data[i][j] == 'B':
                max_neigbor = get_max_neighbor(fronts, (i, j))
                if max_neigbor <= 0:
                    curr_max += 1
                    set_neighbors_except(fronts, (i, j), curr_max, -1)
                else:
                    set_neighbors_except(fronts, (i, j), max_neigbor, -1)
    return fronts

def wumpus():
    """
    fronts = table with fronts, 0 nothing, -1 no front coz O in sensor, >= 1 fronts
    """
    with open(sys.argv[1], "r") as input_f:
        input = input_f.readlines()
    n, m = map(int, input[0].strip().split(' '))
    prob_hole = float(input[1])
    data = np.array([list(line.strip()) for line in input[2:]])

    fronts = get_fronts(data)
    print(fronts)
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
