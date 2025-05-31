#!/usr/bin/env python

def get_frequency(phrase: str) -> None:
    """
    Counts the frequencies of different characters in a string
    and returns a dictionary with their frequency
    """
    
    freq_dictionary = {}
    phrase = "".join(phrase.split())    # remove whitespace

    # send to lower case to avoid errors
    for letter in phrase.lower():
        if letter not in freq_dictionary:   # if character is not in the dictionary, add it
            freq_dictionary[letter] = 1
        else:
            freq_dictionary[letter] += 1    # if character is in the dictionary, increment its value by1

    return freq_dictionary


def main() -> None:

    phrase = input("Enter a phrase: ")

    freq_dictionary = get_frequency(phrase)
    min_frequency = min(freq_dictionary.values())

    # iterate through the dictionary and compare each value with the minimum.
    for key, value in freq_dictionary.items():
        if value == min_frequency:
            print(f"{key}: {value} times")


if __name__ == "__main__":
    main()
