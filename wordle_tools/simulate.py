import functools
import itertools
import json

import heuristic_guess
import lexicon
import matches


@functools.cache
def first_guess(resp, guess):
    candidates = tuple(
        filter(
            lambda s: resp == matches.matches(s, guess),
            lexicon.lexicon,
        )
    )
    next_guess = (
        candidates[0]
        if len(candidates) == 1
        else heuristic_guess.guess(
            guesses=lexicon.lexicon,
            targets=candidates,
        )
    )
    return next_guess, candidates


def game(target, initial_guess):
    guess = initial_guess
    hist = []
    # Unwind first guess for cacheing
    resp = matches.matches(
        target=target,
        guess=guess,
    )
    hist.extend([guess, resp])
    if resp == "22222":
        return hist
    guess, candidates = first_guess(resp, guess)
    for i in itertools.count(start=1):
        resp = matches.matches(
            target=target,
            guess=guess,
        )
        hist.extend([guess, resp])
        if resp == "22222":
            return hist
        candidates = tuple(
            filter(
                lambda s: resp == matches.matches(s, guess),
                candidates,
            )
        )
        guess = (
            candidates[0]
            if len(candidates) == 1
            else heuristic_guess.guess(
                guesses=lexicon.lexicon,
                targets=candidates,
            )
        )
    return ["ERROR"]


def main():
    for w in ["kills"]:  # lexicon.lexicon:
        g = game(
            target=w,
            initial_guess="rotes",
        )
        print(
            w,
            len(g) // 2,
            json.dumps(g),
            sep="\t",
        )


if __name__ == "__main__":
    main()
