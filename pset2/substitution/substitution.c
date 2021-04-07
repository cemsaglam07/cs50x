#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // Checks if the user input is a valid command-line argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // Checks if the user input is a valid key
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    // Checks if the key includes invalid characters
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isalpha((int)(argv[1][i])) == 0)
        {
            printf("Key must contain alphabetic characters.\n");
            return 1;
        }
    }
    // Checks if the key includes duplicate characters
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        for (int j = 0; j < strlen(argv[1]); j++)
        {
            if (i != j && argv[1][i] == argv[1][j])
            {
                return 1;
            }
        }
    }
    // Stores key in a variable for convenience
    string key = argv[1];
    // Prompts the user for a string of plaintext
    string plaintext = get_string("plaintext: ");
    // Outputs the plaintext’s corresponding ciphertext
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if ((int)(plaintext[i]) >= 97 && (int)(plaintext[i]) <= 122)
        {
            // If lowercase, select appropriate cipher and turn lowercase
            printf("%c", tolower((int)(key[(int)(plaintext[i]) - 97])));
        }
        else if ((int)(plaintext[i]) >= 65 && (int)(plaintext[i]) <= 90)
        {
            // If uppercase, select appropriate cipher and turn uppercase
            printf("%c", toupper((int)(key[(int)(plaintext[i]) - 65])));
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
    return 0;
}
