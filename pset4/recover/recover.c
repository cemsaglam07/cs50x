#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        // Syntax message
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        // Error message
        printf("Forensic image cannot be opened for reading\n");
        return 1;
    }
    // Definitions:
    BYTE buffer[512]; // 512 bytes of data will be read per instructions
    FILE *jpeg; // There is no JPEG output yet
    int jpeg_no = 0; // JPEG filemame count
    char name[8]; // File name has 7 characters (0xx.jpg)...
    name[7] = '\0'; // ...and a null terminating char at the end.
    bool jpeg_found = false; // check if previous JPEG exists

    // "Repeat until end of card"
    while (fread(buffer, 512, 1, card))
    {
        // If start of a new JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            // If it's your first JPEG file... (thus no previous JPEGs)
            if (!jpeg_found)
            {
                jpeg_found = true;
            }
            else
            {
                // If not first JPEG file, then close previous one
                // to avoid meddling in other pictures
                fclose(jpeg);
            }

            // Write your new file
            sprintf(name, "%03i.jpg", jpeg_no);
            jpeg = fopen(name, "w");
            if (jpeg == NULL)
            {
                return 1;
            }
            fwrite(buffer, 512, 1, jpeg);
            jpeg_no++;
        }
        else if (jpeg_found == true)
        {
            // Keep writing the file
            fwrite(buffer, 512, 1, jpeg);
        }
    }

    // Close any remaining files
    fclose(jpeg);
    fclose(card);
    return 0;
}
