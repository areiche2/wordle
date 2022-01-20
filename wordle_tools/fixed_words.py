import random

import lexicon
import matches

# all_matches = {
#    (t, g): matches.matches(target=t, guess=g)
#    for t, g in itertools.product(lexicon.lexicon, repeat=2)
# }

for i in range(10000000):
    if i % 10000 == 0:
        print(f"Round {i}")
    words = ["tares", "cough", "blimp", "windy"]
    words.extend(random.sample(lexicon.lexicon, 3))
    combos = {}
    for w in lexicon.daily_words:
        c = tuple(matches.matches(target=w, guess=g) for g in words)
        if c in combos:
            break
        combos[c] = w
    else:
        print("Words: ", words)
        print("All Unique")
        exit()
