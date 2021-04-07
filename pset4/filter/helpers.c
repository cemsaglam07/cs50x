#include "helpers.h"
#include <stddef.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int rgbtSum = image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue;
            int rgbtAvg = (int)(round((double)rgbtSum / 3.0));
            image[i][j].rgbtRed = rgbtAvg;
            image[i][j].rgbtGreen = rgbtAvg;
            image[i][j].rgbtBlue = rgbtAvg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    // For every row
    for (int i = 0; i < height; i++)
    {
        // Swap every column
        int j_down = width - 1;
        for (int j = 0; j < (width / 2); j++)
        {
            // You know the drill...
            temp = image[i][j];
            image[i][j] = image[i][j_down];
            image[i][j_down] = temp;
            j_down--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Defined values:
    RGBTRIPLE blurred_image[height][width];
    int redAvg = 0;
    int greenAvg = 0;
    int blueAvg = 0;
    int avgElementCount = 0;

    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // and copy all pixels to a blur template
            blurred_image[i][j] = image[i][j];
        }
    }

    // Take averages for each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Sum all RGBT values by iterating through +/-1 pixels
            for (int a = i - 1; a <= i + 1; a++)
            {
                for (int b = j - 1; b <= j + 1; b++)
                {
                    // Check if not out of bound
                    if (0 <= a && 0 <= b && a < height && b < width)
                    {
                        // Add RGBT values to sum variable
                        redAvg += image[a][b].rgbtRed;
                        greenAvg += image[a][b].rgbtGreen;
                        blueAvg += image[a][b].rgbtBlue;
                        // Increment the calculated element value by 1
                        avgElementCount++;
                    }
                }
            }

            // Average the sum variable and...
            // ...update pixel RGBT values accordingly
            blurred_image[i][j].rgbtRed = (int)(round((double)redAvg / (double)avgElementCount));
            blurred_image[i][j].rgbtGreen = (int)(round((double)greenAvg / (double)avgElementCount));
            blurred_image[i][j].rgbtBlue = (int)(round((double)blueAvg / (double)avgElementCount));

            // Reset variables for re-usage
            redAvg = 0;
            greenAvg = 0;
            blueAvg = 0;
            avgElementCount = 0;
        }
    }

    // Replace the template with the normal one
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // and copy all pixels to a blur template
            image[i][j] = blurred_image[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Defined values:
    RGBTRIPLE edge_image[height][width];
    int redGx = 0, greenGx = 0, blueGx = 0;
    int redGy = 0, greenGy = 0, blueGy = 0;
    int redE = 0, greenE = 0, blueE = 0;
    int Gx_array[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int Gy_array[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    int n = 0; // n = array index value

    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // and set default value to 255
            // value will be change if in range of 0-255
            edge_image[i][j].rgbtRed = 255;
            edge_image[i][j].rgbtBlue = 255;
            edge_image[i][j].rgbtGreen = 255;
        }
    }

    // Calculate Gx & Gy values
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // For each pixel, iterate through +/-1 pixels
            for (int a = i - 1; a <= i + 1; a++)
            {
                for (int b = j - 1; b <= j + 1; b++)
                {
                    // Check if not out of bound
                    if (0 <= a && 0 <= b && a < height && b < width)
                    {
                        redGx += (Gx_array[n] * image[a][b].rgbtRed);
                        greenGx += (Gx_array[n] * image[a][b].rgbtGreen);
                        blueGx += (Gx_array[n] * image[a][b].rgbtBlue);

                        redGy += (Gy_array[n] * image[a][b].rgbtRed);
                        greenGy += (Gy_array[n] * image[a][b].rgbtGreen);
                        blueGy += (Gy_array[n] * image[a][b].rgbtBlue);
                    }
                    n++;
                }
            }

            // Calculate RGBT values by sqrt(Gx * Gx + Gy * Gy)
            redE = (int)(round(sqrt((double)((redGx * redGx) + (redGy * redGy)))));
            greenE = (int)(round(sqrt((double)((greenGx * greenGx) + (greenGy * greenGy)))));
            blueE = (int)(round(sqrt((double)((blueGx * blueGx) + (blueGy * blueGy)))));

            // Cap values to 255, if excess amount
            if (redE >= 0 && redE <= 255)
            {
                edge_image[i][j].rgbtRed = redE;
            }
            if (greenE >= 0 && greenE <= 255)
            {
                edge_image[i][j].rgbtGreen = greenE;
            }
            if (blueE >= 0 && blueE <= 255)
            {
                edge_image[i][j].rgbtBlue = blueE;
            }
            // Reset all variables for loop re-usage
            redE = 0, greenE = 0, blueE = 0, n = 0;
            redGx = 0, greenGx = 0, blueGx = 0;
            redGy = 0, greenGy = 0, blueGy = 0;
        }
    }

    // Replace the template with the normal one
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // and copy all pixels to a blur template
            image[i][j] = edge_image[i][j];
        }
    }
}
