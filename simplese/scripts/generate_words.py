from itertools import product

consonants = ["p", "t", "k"]
vowels = ["a", "i", "u"]

syllables = [c + v for c in consonants for v in vowels]
stressed_syllables = ["'" + s for s in syllables]

# monosyllables = ["'" + s for s in all_syllables]
# disyllables = ["'" + s1 + "." + s2 for s1 in all_syllables for s2 in all_syllables] + [
#     s1 + "." + "'" + s2 for s1 in all_syllables for s2 in all_syllables
# ]


def generate_words(n_syllables):
    for stress in range(n_syllables):
        syllable_set = (
            [syllables] * stress
            + [stressed_syllables]
            + [syllables] * (n_syllables - stress - 1)
        )
        for word in product(*syllable_set):
            yield ".".join(word)


# words = monosyllables + disyllables

for n_syllables in range(1, 3):
    for word in generate_words(n_syllables):
        print(word)
