from cs50 import get_string


def main():
    text = get_string("Text: ")

    # Calculate the index of the given text:
    L = (count_letters(text) * 100.0) / float(count_words(text))
    S = (count_sentences(text) * 100.0) / float(count_words(text))
    index = int(round((0.0588 * L) - (0.296 * S) - 15.8))

    # Print values according to their indices:
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def count_letters(text):
    letter_count = 0
    for i in range(0, len(text)):
        # Checks if the chosen character is a letter with ASCII table
        if (ord(text[i]) <= 90 and ord(text[i]) >= 65) or (ord(text[i]) >= 97 and ord(text[i]) <= 122):
            letter_count += 1
    return letter_count


def count_words(text):
    word_count = 1
    for i in range(0, len(text)):
        # Checks if the chosen character is a space
        if text[i] == " ":
            word_count += 1
    return word_count


def count_sentences(text):
    sentence_count = 0
    for i in range(0, len(text)):
        # Checks if the chosen character is an punctuation
        if text[i] in [".", "!", "?"]:
            sentence_count += 1
    return sentence_count


main()