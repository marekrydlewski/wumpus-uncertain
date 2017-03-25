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


def get_possible_areas(data):
    y, x = input.shape
    possible = np.zeros((y, x), dtype=bool) #sets true

    for i in range(x):
        for j in range(y):
            if data[i][j] == 'O':
                possible[i][j] = False
                set_neighbors(possible, (i, j), False)

    return possible


def get_fronts(data, possible):
    y, x = input.shape
    fronts = np.zeros((y, x), dtype=int)

    for i in range(x):
        for j in range(y):
            if data[i][j] == 'O':
                fronts[i][j] = -1
                set_neighbors(fronts, (i, j))
            elif data[i][j] == 'B':
                fronts[i][j] = -1

            elif data[i][j] == '?':
                curr_front = fronts[i][j]
                if curr_front != -1:
                    pass
            else:
                print("Unrecognized type in wumpus input")

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

    possible_areas = get_possible_areas(data)

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
