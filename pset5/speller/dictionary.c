// Implements a dictionary's functionality
#include <stdbool.h> // bool
#include "dictionary.h"
#include <ctype.h> // toupper
#include <strings.h> // strcasecmp
#include <string.h> // strcpy
#include <stdio.h>
#include <stdlib.h> // malloc

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

const unsigned int N = 11881376; // 26 ^ 5 == 11881376
unsigned int hash_value; // Hash value
unsigned int word_count; // Word count for size()
node *hash_table[N]; // Hash table


// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain a hash value
    hash_value = hash(word);
    // Access linked list at that index in the hash table
    node *cursor = hash_table[hash_value];
    // Until you get to NULL...
    while (cursor != NULL)
    {
        // Traverse linked list, looking for the word (strcasecmp)
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        // Keep moving cursor checking each node for the word
        cursor = cursor->next;
    }
    // Return false if cannot be found
    return false;
}

// Hashes word to a number
// Source: http://www.cse.yorku.ca/~oz/hash.html
// Source found after googling "Hash Functions"
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = toupper(*word++)))
    {
        hash = ((hash << 5) + hash) + c;
    }
    return hash % N;
}

// TODO: Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Set the buckets as NULL for starters
    for (int i = 0; i < N; i++)
    {
        hash_table[i] = NULL;
    }

    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fclose(file);
        return false;
    }

    // Initialize "word" for the fscanf next line
    char word[LENGTH + 1];
    // Read strings from file one at a time
    while (fscanf(file, "%s", word) != EOF)
    {
        // Create new node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        // Copy word into node using strcpy
        // strcpy(destination, source)
        strcpy(n->word, word);
        // Hash word to obtain a hash value
        hash_value = hash(word);
        // Set the next value of node "n"
        n->next = hash_table[hash_value];
        // Insert node into hash table at that location
        hash_table[hash_value] = n;
        // Word count for size() function
        word_count += 1;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Word count was already initialized in header
    // and was incremented in load()
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate through all buckets and free their nodes
    for (int i = 0; i < N; i++)
    {
        // Create a cursor for the bucket "i"
        node *cursor = hash_table[i];
        while (cursor != NULL)
        {
            // Create a temporary second cursor
            node *tmp = cursor;
            // Slide the cursor to the next node
            cursor = cursor->next;
            // Free tmp and its pointing node
            free(tmp);
        }

        // if cursor is slided into null
        // and if we have cleared all buckets (index: N-1)
        if ((cursor == NULL) && (i == (N - 1)))
        {
            return true;
        }
    }
    // If something is wrong, return false:
    return false;
}
