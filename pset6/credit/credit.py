from math import log10
from math import floor


def main():
    # Get the credit card digits
    credit_card = int(input("Number: "))

    # Find digit count, inspired from Wikipedia Article: Logarithm
    card_length = int(floor(log10(credit_card) + 1))

    # Checksum Algorithm
    checksum_result = checksum_check(credit_card, card_length)

    # Starting Number Check
    # @return AMEX = 1 MASTERCARD = 2 VISA = 3 INVALID = 4
    starting_num_result = start_num_check(credit_card, card_length)

    # Print results!
    if checksum_result == 0 and starting_num_result == 1:
        print("AMEX")
    elif checksum_result == 0 and starting_num_result == 2:
        print("MASTERCARD")
    elif checksum_result == 0 and starting_num_result == 3:
        print("VISA")
    else:
        print("INVALID")


def get_digit(num, d_raw):
    d = pow(10.0, d_raw)
    d_1 = pow(10.0, d_raw + 1)
    x1 = num % int(d_1)
    x2 = num % int(d)
    return int((x1 - x2) / d)


def checksum_check(card, length):
    sum1 = 0
    sum2 = 0
    is_second_digit = False
    for i in range(0, length):
        digit = get_digit(card, i)
        if is_second_digit:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
            sum1 += digit
        else:
            sum2 += digit
        is_second_digit = not is_second_digit
    return (sum1 + sum2) % 10


def start_num_check(card, length):
    sn = find_starting_num(card, length)
    visa_sn = get_digit(card, length - 1)

    # CARD NAME            LENGTH              STARTING NUMBERS        RETURN VALUE
    # American Express  = 15-digit         = 34 or 37              =       1
    # MasterCard        = 16-digit         = 51, 52, 53, 54, or 55 =       2
    # Visa              = 13 or 16-digit   = 4                     =       3

    if length == 15 and (sn in [34, 37]):
        return 1  # AMERICAN EXPRESS
    elif length == 16 and (sn in [51, 52, 53, 54, 55]):
        return 2  # MASTERCARD
    elif visa_sn == 4 and (length in [13, 16]):
        return 3  # VISA
    else:
        return 4


def find_starting_num(card, length):
    x1 = get_digit(card, length - 1)
    x2 = get_digit(card, length - 2)
    return (10 * x1) + x2


main()