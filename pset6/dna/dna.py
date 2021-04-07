import csv  # CSV files
import sys  # Command-line arguments


def main():
    # Check the number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python dna.py DATABASE SEQUENCE")
        sys.exit(1)

    # Read contents of CSV file
    people = {}
    with open(sys.argv[1], "r") as file:
        # Set the reader
        reader = csv.reader(file)
        for row in reader:
            # For titles, copy all STR values into "strs"
            if str(row[0]) == "name":
                strs = row[1:len(row)]
            # For people, copy their values into dict "people"
            else:
                # Lists are unhashable types; convert into strings via repr()
                people[repr([int(i) for i in row[1:len(row)]])] = str(row[0])

    # Read contents of DNA sequence
    with open(sys.argv[2], "r") as file:
        seq = file.readline()

    # Compute the longest run of consecutive repeats
    profile = []
    for repeat in strs:
        x = 1
        loop = True
        while loop == True:
            if seq.count(repeat * x) > 0:
                x += 1
            else:
                x = x - 1
                loop = False
        profile.append(x)

    # Compare STR profile to people
    if repr(profile) in people.keys():
        print(people[repr(profile)])
    else:
        print("No match")


main()