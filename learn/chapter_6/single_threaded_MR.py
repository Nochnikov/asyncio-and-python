import functools


def map_frequency(text: str) -> dict[str, int]:
    words = text.split(' ')
    frequencies = {}

    for word in words:
        if word in frequencies:
            """
            if we have the word in our frequency dictionary, 
            add one to the count. 
            """
            frequencies[word] += 1
        else:
            """
            if we do not have the word in our frequency dictionary, 
            set its count to one.
            """
            frequencies[word] = 1

    return frequencies

def merge_dictionaries(
    first: dict[str, int],
    second: dict[str, int],
):
    merged = first

    for key in second:
        if key in merged:
            """if the word is in both dictionaries, combine frequency counts"""
            merged[key] = merged[key] + second[key]
        else:
            """If the word is not in both dictionaries,
            copy over the frequency count"""
            merged[key] = second[key]

    return merged

lines = {
    "I know what I know",
    "I know what I know",
    "I don't know much",
    "They don't know much"
}
"""For each line of text, perform our map operation."""
mapped_results = [map_frequency(line) for line in lines]

for result in mapped_results:
    print(result)

"""Reduce all our intermediate frequency counts into one result"""
print(functools.reduce(merge_dictionaries, mapped_results))