import sys
import numpy as np


def wumpus():
    with open(sys.argv[1], "r") as input_f:
        input = input_f.readlines()

    n, m = map(int, input[0].strip().split(' '))
    prob_hole = float(input[1])
    data = np.array([list(line.strip()) for line in input[2:]])

    output = np.zeros((n, m), float)

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
