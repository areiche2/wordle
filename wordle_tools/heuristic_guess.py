import collections

import matches


def scores_it(guesses, targets):
    return (
        (w, max(collections.Counter(guess).values()))
        for w, guess in zip(
            guesses,
            matches.matches_table(
                guesses=guesses,
                targets=targets,
            ),
        )
    )


def guess(guesses, targets):
    if len(guesses) == 1:
        return guesses[0]
    return min(
        scores_it(
            guesses=guesses,
            targets=targets,
        ),
        key=lambda o: o[1],
    )[0]
