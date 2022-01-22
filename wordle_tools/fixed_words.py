import collections
import itertools
import json

import lexicon
import matches


def get_combos(p):
    combos = collections.defaultdict(list)
    for w in lexicon.daily_words:
        c = tuple(matches.matches(target=w, guess=g) for g in p)
        combos[c].append(w)
    return combos


def score(p):
    combos = get_combos(p)
    return sum(1 if len(b) == 1 else 2 for b in combos.values())


def get_scores():
    p = ("brake", "dying", "clots", "whump")
    res = {}
    res[p] = score(p)
    for subset in itertools.combinations(p, len(p) - 1):
        for w in lexicon.lexicon:
            if w not in p:
                neighbor = subset + (w,)
                res[neighbor] = score(neighbor)
    return res


if __name__ == "__main__":
    res = get_scores()
    best = max(res.items(), key=lambda x: x[1])
    print(
        json.dumps(
            {
                "words": best[0],
                "score_n": best[1],
                "score_d": len(lexicon.daily_words),
                "signatures": {
                    "-".join(resp): sorted(ws)
                    for resp, ws in get_combos(best[0]).items()
                },
            },
            sort_keys=True,
            indent=4,
        )
    )
