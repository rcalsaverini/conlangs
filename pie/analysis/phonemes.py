import re
from pregex.core.classes import AnyFrom
from pregex.core.quantifiers import AtLeastAtMost, OneOrMore, Optional, Indefinite
from pregex.core.operators import Either
from pregex.core.groups import Capture
from pregex.core.pre import Pregex

SIMPLE_VOWELS = AnyFrom("a", "e", "i", "o", "u")
STRESSED_VOWELS = AnyFrom("á", "é", "í", "ó", "ú")
LONG_VOWELS = Either(SIMPLE_VOWELS + Pregex("ː"), STRESSED_VOWELS + Pregex("ː"))
ANY_SINGLE_VOWEL = Either(LONG_VOWELS, STRESSED_VOWELS, SIMPLE_VOWELS)
DIPTHONGS = AtLeastAtMost(ANY_SINGLE_VOWEL, 2, 3)


LARYNGEALS = Pregex("h") + AnyFrom("₁", "₂", "₃")
RHOTICS = AnyFrom("r", "ɹ", "ɾ")
LIQUIDS = AnyFrom("l", "ɭ", "ʎ", "ɫ")
NASALS = AnyFrom("m", "n", "ŋ")
GLIDES = AnyFrom("y", "w")
SIBILANTS = AnyFrom("s", "z", "ʃ", "ʒ")
STOPS = AnyFrom("p", "b", "t", "d", "k", "g", "q")
FRICATIVES = AnyFrom("f", "v", "θ", "ð", "x", "ɬ", "ɮ")
AFFRICATES = Either("ts", "dz", "tʃ", "dʒ", "tɬ", "dɮ", "tç", "dʝ")
PALATALIZED = STOPS + Pregex("ʲ")
VELARIZED = STOPS + Pregex("ˠ")
ASPIRATED = STOPS + Pregex("ʰ")
LABIALIZED = STOPS + Pregex("ʷ")



VOWEL_LIKE = Capture(Either(ANY_SINGLE_VOWEL, DIPTHONGS))
SIBILANT = Capture(SIBILANTS)
GLIDE = Capture(GLIDES)
NASAL = Capture(NASALS)
LIQUID = Capture(LIQUIDS)
LARYNGEAL = Capture(LARYNGEALS)
RHOTIC = Capture(RHOTICS)
CONSONANT = Capture(Either(VELARIZED, PALATALIZED, ASPIRATED, LABIALIZED, RHOTICS, LIQUIDS, NASALS, GLIDES, SIBILANTS, STOPS, FRICATIVES, AFFRICATES))

SYLLABLE_SEPARATOR = Pregex(".")

SYLLABLE = Either(
    (CONSONANT + CONSONANT.optional(is_greedy=False) + VOWEL_LIKE + CONSONANT.optional(is_greedy=False) + CONSONANT.optional(is_greedy=False)),
    CONSONANT.optional(is_greedy=False) + LARYNGEAL + CONSONANT.optional(is_greedy=False),
)

WORD = (
    SYLLABLE.capture("syllable").match_at_start() + 
    Indefinite(SYLLABLE, is_greedy=False)\
        .capture("rest").match_at_end()
)

regexes = {
    "VOWEL_LIKE": re.compile(VOWEL_LIKE.get_pattern()),
    "CONSONANT": re.compile(CONSONANT.get_pattern()),
    "LARYNGEAL": re.compile(LARYNGEAL.get_pattern()),
    "SYLLABLE_SEPARATOR": re.compile(SYLLABLE_SEPARATOR.get_pattern()),
}

def parse_word(word):
    syllables = []    
    rest = word
    while len(rest) > 0:
        captures = WORD.get_named_captures(rest)
        print(rest, captures)
        for capture in captures:
            rest = capture["rest"]
            syllables.append(capture["syllable"])

rest = "ph₂teːr"
while len(rest) > 0:
    captures = WORD.get_named_captures(rest)
    for capture in captures:
        rest = capture["rest"]
        print(capture["syllable"])