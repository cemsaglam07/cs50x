#include <stdio.h>
#include <cs50.h>
#include <math.h>
double pow(double x, double y);
long double powl(long double base, long double exponent);
int get_digit(long num, int d_raw);
int checksum_check(long card, int length);
int start_num_check(long card, int length);
int find_starting_num(long card, int length);


int main(void)
{
    // Get the credit card digits
    long credit_card = get_long("Number: ");

    // Find digit count, inspired from Wikipedia Article: Logarithm
    int card_length = (int)floor(log10(credit_card) + 1);

    // Checksum Algorithm
    int checksum_result = checksum_check(credit_card, card_length);

    // Starting Number Check
    // @return AMEX = 1 MASTERCARD = 2 VISA = 3 INVALID = 4
    int starting_num_result = start_num_check(credit_card, card_length);

    // Print results!
    if (checksum_result == 0 && starting_num_result == 1)
    {
        printf("AMEX\n");
    }
    else if (checksum_result == 0 && starting_num_result == 2)
    {
        printf("MASTERCARD\n");
    }
    else if (checksum_result == 0 && starting_num_result == 3)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

int get_digit(long num, int d_raw)
{
    long double d = powl(10.0, (double)d_raw);
    long double d_1 = powl(10.0, (double)(d_raw + 1));
    long x1 = num % (long)d_1;
    long x2 = num % (long)d;
    long x3 = x1 - x2;
    int x4 = (int)(x3 / d);
    return x4;
}

int checksum_check(long card, int length)
{
    int sum1 = 0;
    int sum2 = 0;
    bool is_second_digit = false;
    for (int i = 0; i < length; i++)
    {
        int digit = get_digit(card, i);
        if (is_second_digit)
        {
            digit = digit * 2;
            if (digit > 9)
            {
                digit = digit - 9;
            }
            sum1 += digit;
        }
        else
        {
            sum2 += digit;
        }
        is_second_digit = (!(is_second_digit));
    }
    int result = (sum1 + sum2) % 10;
    return result;
}

int start_num_check(long card, int len)
{
    int sn = find_starting_num(card, len);
    int visa_sn = get_digit(card, len - 1);

    // CARD NAME            LENGTH              STARTING NUMBERS        RETURN VALUE
    // American Express  = 15-digit         = 34 or 37              =       1
    // MasterCard        = 16-digit         = 51, 52, 53, 54, or 55 =       2
    // Visa              = 13 or 16-digit   = 4                     =       3

    if (len == 15 && (sn == 34 || sn == 37))
    {
        return 1; // AMERICAN EXPRESS
    }
    else if (len == 16 && (sn == 51 || sn == 52 || sn == 53 || sn == 54 || sn == 55))
    {
        return 2; // MASTERCARD
    }
    else if (visa_sn == 4 && (len == 13 || len == 16))
    {
        return 3; // VISA
    }
    else
    {
        return 4;
    }
}

int find_starting_num(long card, int length)
{
    int x1 = get_digit(card, length - 1);
    int x2 = get_digit(card, length - 2);
    return (10 * x1) + x2;
}
