import collections
import json

import lexicon
import matches

# all_matches = {
#    (t, g): matches.matches(target=t, guess=g)
#    for t, g in itertools.product(lexicon.lexicon, repeat=2)
# }

words = ["brake", "dying", "clots", "whump"]
combos = collections.defaultdict(list)
for w in lexicon.daily_words:
    c = tuple(matches.matches(target=w, guess=g) for g in words)
    combos[c].append(w)
print(
    json.dumps(
        {
            "-".join(resp): {"words": sorted(ws), "len": len(ws)}
            for resp, ws in combos.items()
        },
        sort_keys=True,
        indent=4,
    )
)
