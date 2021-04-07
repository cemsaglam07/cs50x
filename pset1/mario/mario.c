#include <stdio.h>
#include <cs50.h>

int validate_height(void);

int main(void)
{
    // Gets the valid input and stores it in the variable "height"
    int height = validate_height();

    // Print statement for each line
    for (int i = 1; i <= height; i++)
    {
        // Spaces
        for (int j = 0; j < height - i; j++)
        {
            printf(" ");
        }
        // Bricks
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        // Two space gap
        printf(" ");
        printf(" ");
        // Bricks
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        // New Line
        printf("\n");
    }
}

// Gets the valid input, asks input again if not valid
int validate_height(void)
{
    int n = get_int("Height: ");
    while (n < 1 || n > 8)
    {
        n = get_int("Height: ");
    }
    return n;
}
