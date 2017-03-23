import sys


def wumpus():
    with open(sys.argv[1], "r") as input_f:
        input = input_f.read()

    with open(sys.argv[2], "w+") as output_f:
        pass

    print(input)
    return


def main():
    if len(sys.argv) < 3 or sys.argv[0] == '-h':
        print("Pass proper args")
        exit(0)
    wumpus()


if __name__ == '__main__':
    main()
