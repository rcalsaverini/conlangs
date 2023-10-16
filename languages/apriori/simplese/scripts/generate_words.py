from itertools import product

hard_consonants = ["p", "t", "k"]
soft_consonants = ["m", "s"]
liquids = ["w", "l"]
front_vowels = ["a", "i"]
back_vowels = ["u"]
vowels = front_vowels + back_vowels
consonants = hard_consonants + liquids

cv_syllables = [c + v for c in consonants for v in vowels]
clv_syllables = [
    c + l + v for c in hard_consonants for l in liquids for v in front_vowels
]
cvs_syllables = [
    c + v + s for c in hard_consonants for v in front_vowels for s in soft_consonants
]
syllables = cv_syllables  # + clv_syllables + cvs_syllables
stressed = ["'" + s for s in syllables]

# monosyllables = ["'" + s for s in all_syllables]
# disyllables = ["'" + s1 + "." + s2 for s1 in all_syllables for s2 in all_syllables] + [
#     s1 + "." + "'" + s2 for s1 in all_syllables for s2 in all_syllables
# ]


def generate_words(n_syllables, stress_position):
    syllable_set = [syllables] * n_syllables
    syllable_set[stress_position] = stressed
    for word in product(*syllable_set):
        yield ".".join(word)


# words = monosyllables + disyllables

for n_syllables in range(1, 4):
    for stress_position in range(n_syllables):
        for word in generate_words(n_syllables, stress_position):
            print(word)
