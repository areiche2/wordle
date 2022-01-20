import collections

import matches
from lexicon import lexicon

for w, guess in zip(
    lexicon,
    matches.matches_table(
        guesses=lexicon,
        targets=lexicon,
    ),
):
    print(w, max(collections.Counter(guess).values()), sep="\t")
