import collections
import json

import lexicon
import matches

words = ["brake", "dying", "clots", "whump"]
combos = collections.defaultdict(list)
all_words = lexicon.lexicon
for w in all_words:
    c = tuple(matches.matches(target=w, guess=g) for g in words)
    combos[c].append(w)
print(
    json.dumps(
        {
            "words": words,
            "score_n": sum(1 if len(ws) == 1 else 2 for ws in combos.values()),
            "score_d": len(all_words),
            "signatures": {
                "-".join(resp): {"words": sorted(ws), "len": len(ws)}
                for resp, ws in combos.items()
            },
        },
        sort_keys=True,
        indent=4,
    )
)
