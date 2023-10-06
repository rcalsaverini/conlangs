from dataclasses import dataclass
from typing import List
from gruut_ipa.constants import CONSONANTS, VOWELS


@dataclass()
class Syllable:
    phones: List[str]
    stress: bool

    @property
    def consonants(self):
        _consonants = {chr for chr in self.phones if chr in CONSONANTS}
        return _consonants

    @property
    def vowels(self):
        _vowels = {chr for chr in self.phones if chr in VOWELS}
        return _vowels


def parse_word(word):
    return [
        Syllable(syllable.strip().lstrip("'"), syllable.startswith("'"))
        for syllable in word.split(".")
    ]


with open("../lexurgy/output.wlm", "r") as f:
    WORDS = [line.strip() for line in f.readlines()]
ALL_CONSONANTS = {
    c for word in WORDS for syllable in parse_word(word) for c in syllable.consonants
}

ALL_VOWELS = {
    v for word in WORDS for syllable in parse_word(word) for v in syllable.vowels
}

print("\n".join(ALL_CONSONANTS))
print("\n".join(ALL_VOWELS))
