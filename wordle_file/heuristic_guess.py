import collections

import matches


# Note: Lower score means better
def max_agg(resps):
    return max(
        (w for w in collections.Counter(resps).values() if w != "22222"),
        default=0,
    )


def avg_agg(resps):
    c = collections.Counter(resps)
    return sum(w ** 2 for resp, w in c.items() if resp != "22222")


def scores_it(guesses, targets):
    return (
        (w, avg_agg(resps))
        for w, resps in zip(
            guesses,
            matches.matches_table(
                guesses=guesses,
                targets=targets,
            ),
        )
    )


def guess(guesses, targets, agg=max):
    if len(guesses) == 1:
        return guesses[0]
    return min(
        scores_it(
            guesses=guesses,
            targets=targets,
        ),
        key=lambda o: o[1],
    )[0]
