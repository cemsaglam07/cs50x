#include <stdio.h>
#include <cs50.h>

// This method will ask the users for their names, and say hello to them.
int main(void)
{
    // Gets the user input and stores it in a variable called "name"
    string name = get_string("What is your name?\n");
    // Concentinates the string "hello, " and the string variable "name"
    printf("hello, %s\n", name);
}
