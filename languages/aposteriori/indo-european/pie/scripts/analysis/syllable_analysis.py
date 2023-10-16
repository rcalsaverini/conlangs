from phonemes import *
import pandas as pd
import itertools as it


def get_next_character(word):
    for name, regex in regexes.items():
        match = regex.match(word)
        if match is not None:
            character = match.group()
            rest = word[match.end():]
            return character, name, rest
    else:
        raise ValueError(f"Not Found: {word}")

def get_next_syllable(word):
    syllable_type = []
    syllable_chars = []
    rest = word
    while len(rest) > 0:
        character, name, rest = get_next_character(rest)
        if name == "SYLLABLE_SEPARATOR":
            return "".join(syllable_chars), "".join(syllable_type), rest
        else:
            syllable_chars.append(character)
            syllable_type.append(f"[{name}]")
    else:
        return "".join(syllable_chars), "".join(syllable_type), rest

def word_to_syllables(word):
    syllables = []
    rest = word
    while len(rest) > 0:
        syllable_chars, syllable_type, rest = get_next_syllable(rest)
        syllables.append((syllable_chars, syllable_type))
    return syllables

def group_syllables_by_type(words):
    unique_syllables = sorted({(syl, syl_type) for word in words for syl, syl_type in word_to_syllables(word)}, key=lambda x: (x[1], x[0]))
    return {
        syl_type: list([syl for syl, syl_type in syls])
        for syl_type, syls in it.groupby(unique_syllables, key=lambda x: x[1])
    }
