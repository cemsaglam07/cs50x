from cs50 import get_int


def main():
    # Gets the valid input and stores it in the variable "height"
    height = validate_height()
    # Print statement for each line
    for i in range(1, height + 1):
        # Spaces
        for j in range(0, height - i):
            print(" ", end="")

        # Bricks
        for j in range(0, i):
            print("#", end="")

        # Two space gap
        print(" " * 2, end="")

        # Bricks
        for j in range(0, i):
            print("#", end="")

        print()


# Gets the valid input, asks input again if not valid
def validate_height():
    n = get_int("Height: ")
    while n < 1 or n > 8:
        n = get_int("Height: ")
    return n


main()