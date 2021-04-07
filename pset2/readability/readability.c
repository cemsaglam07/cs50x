#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>
double round(double x);
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get user input
    string text = get_string("Text: ");
    // Find values of L and S
    double L = (((double)(count_letters(text))) * 100.0) / ((double)(count_words(text)));
    double S = (((double)(count_sentences(text))) * 100.0) / ((double)(count_words(text)));
    // Calculate index
    int index = (int)round((0.0588 * L) - (0.296 * S) - 15.8);
    // Print them!
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int letter_count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        // Checks if the chosen character is a letter with ASCII table
        if (((int)text[i] <= 90 && (int)text[i] >= 65) || ((int)text[i] >= 97 && (int)text[i] <= 122))
        {
            letter_count += 1;
        }
    }
    return letter_count;
}

int count_words(string text)
{
    int word_count = 1;
    // Checks if the chosen character is a space with ASCII table
    for (int i = 0; i < strlen(text); i++)
    {
        if ((int)text[i] == ' ')
        {
            word_count += 1;
        }
    }
    return word_count;
}

int count_sentences(string text)
{
    int sentence_count = 0;
    // Checks if the chosen character is an punctuation with ASCII table
    for (int i = 0; i < strlen(text); i++)
    {
        if ((int)text[i] == '.' || (int)text[i] == '!' || (int)text[i] == '?')
        {
            sentence_count += 1;
        }
    }
    return sentence_count;
}
