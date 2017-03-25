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

    for k, v in breeze_checked.items():
        if v == False:
            return False
    return True


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
                max_neighbor = get_max_neighbor(fronts, (i, j))
                if max_neighbor <= 0:
                    curr_max += 1
                    neighbors = set_neighbors_except(fronts, (i, j), curr_max, -1)
                    breeze_in_fronts[i][j] = curr_max

                    front_indexes[curr_max].extend(neighbors)
                    breeze_indexes[curr_max].append((i, j))
                else:
                    neighbors = set_neighbors_except(fronts, (i, j), max_neighbor, -1)
                    breeze_in_fronts[i][j] = max_neighbor

                    front_indexes[max_neighbor].extend(neighbors)
                    breeze_indexes[max_neighbor].append((i, j))

    for k, v in front_indexes.items():
        temp_set = set(v)
        front_indexes[k] = list(temp_set)

    return fronts, breeze_in_fronts, front_indexes, breeze_indexes

def set_prob(prob, factor):
    if prob == 0.0:
        return factor
    else:
        return prob * factor

def compute_probability(breeze_possible, trap_table, current, prob):
    final_prob_left = 0.0
    final_prob_right = 0.0
    y, x = trap_table.shape

    for breeze, traps in zip(breeze_possible, trap_table):
        if breeze == True:
            local_prob_left = 0.0
            local_prob_right = 0.0
            for index, trap in enumerate(traps):
                if index != current:
                    if traps[current] == True:
                        #prob left
                        if trap == True:
                            local_prob_left = set_prob(local_prob_left, prob)
                        else:
                            local_prob_left = set_prob(local_prob_left, 1 - prob)
                    else:
                        #prob right
                        if trap == True:
                            local_prob_right = set_prob(local_prob_right, prob)
                        else:
                            local_prob_right = set_prob(local_prob_right, 1 - prob)

            final_prob_left += local_prob_left
            final_prob_right += local_prob_right

    final_prob_left *= prob
    final_prob_right *= (1 - prob)
    
    #normalization
    sum = final_prob_right + final_prob_left
    return round(final_prob_left / sum , 2), round(final_prob_right / sum, 2)


def wumpus():
    """
    fronts = table with fronts, 0 nothing (normal probability), -1 no front coz O in sensor, >= 1 fronts
    """
    with open(sys.argv[1], "r") as input_f:
        input = input_f.readlines()
    n, m = map(int, input[0].strip().split(' '))
    prob_trap = float(input[1])
    data = np.array([list(line.strip()) for line in input[2:(2 + n)]])

    fronts, breezes, front_indexes, breeze_indexes = get_fronts(data)
    print(fronts)
    print(front_indexes)
    print()
    print(breezes)
    print(breeze_indexes)
    print()


    output = np.zeros((n, m), dtype=float)

    for k, front in front_indexes.items():
        breeze = breeze_indexes[k]
        trap_table = get_combinations(len(front))
        print("breeze: ", breeze, " fronts: ", front)
        breeze_possible = list()
        for traps in trap_table:  # check one variant of trap setting
            breeze_possible.append(get_breeze_checked(breeze, traps, front))

        print(breeze_possible)
        print(trap_table)

        for f in range(len(front)):
            fp = compute_probability(breeze_possible, trap_table, f, prob_trap)
            print(fp)


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
