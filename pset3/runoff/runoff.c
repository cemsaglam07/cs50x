#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    for (int candidate_index = 0; candidate_index < candidate_count; candidate_index++)
    {
        // "If name is a match for the name of a valid candidate..."
        if (strcmp(name, candidates[candidate_index].name) == 0)
        {
            // "...then you should update the global preferences array..."
            // "...to indicate that the voter voter has that candidate as their rank preference."
            preferences[voter][rank] = candidate_index;
            return true;
        }
    }
    // "If the preference is NOT successfully recorded, return false"
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // "every voter effectively votes..."
    for (int voter = 0; voter < voter_count; voter++)
    {
        int rank = 0; // "...for their top-preferred candidate..."
        while (rank != -1)
        {
            // "...who has not already been eliminated."
            if (candidates[preferences[voter][rank]].eliminated == false)
            {
                // "update the number of votes each candidate has"
                candidates[preferences[voter][rank]].votes += 1;
                // Stop the while loop by nullifying rank
                rank = -1;
            }
            else
            {
                // If not correct, we can try again by incrementing rank
                rank += 1;
            }
        }
    }
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > (voter_count / (float)2))
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    int min;
    // Declare min value
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].eliminated == false)
        {
            min = candidates[i].votes;
            break;
        }
    }

    // Update the minimum value
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].eliminated == false && candidates[i].votes < min)
        {
            min = candidates[i].votes;
        }
    }

    // Finalize & return
    return min;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].eliminated == false && candidates[i].votes != min)
        {
            return false;
        }
    }
    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    if (!is_tie(min))
    {
        for (int i = 0; i < candidate_count; i++)
        {
            if (min == candidates[i].votes)
            {
                candidates[i].eliminated = true;
            }
        }
    }
    return;
}
