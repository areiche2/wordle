import argparse
import collections
import json
import random
import re

import heuristic_guess
import lexicons
import matches


def expand_graph(lexicon, is_hard_mode, candidates, is_random, depth):
    if not candidates:
        raise ValueError("Error: No candidates.")
    if len(candidates) == 1:
        return {
            "guess": candidates[0],
            "response": {},
            "depth": depth,
            "candidates": candidates,
        }
    guesses = candidates if is_hard_mode else lexicon
    guess = (
        random.choice(guesses)
        if is_random
        else heuristic_guess.guess(
            guesses=guesses,
            targets=candidates,
        )
    )
    gather = collections.defaultdict(list)
    for c in candidates:
        gather[matches.matches(target=c, guess=guess)].append(c)
    return {
        "guess": guess,
        "response": {
            resp: expand_graph(
                lexicon,
                is_hard_mode,
                grp,
                is_random,
                depth + 1,
            )
            for resp, grp in gather.items()
            if not re.fullmatch("2+", resp)
        },
        "depth": depth,
        "candidates": sorted(candidates),
    }


def main(lexicon, candidates, is_hard_mode, is_random, regexp):
    if regexp:
        candidates = [w for w in candidates if re.search(regexp, w)]
    res = expand_graph(
        lexicon,
        is_hard_mode,
        candidates,
        is_random,
        0,
    )
    print(json.dumps(res))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Wordle File Generator")
    parser.add_argument(
        "--hard-mode",
        action="store_true",
        help="Only guess potential candidates",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Random guesses",
    )
    parser.add_argument(
        "--regexp",
        action="store",
        help="Regular expression filter. Applied after --restricted",
        type=str,
    )
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument(
        "--wordle-daily",
        action="store_const",
        const=(
            lexicons.wordle.lexicon,
            lexicons.wordle.daily_words,
        ),
        dest="solution_space",
        help="Wordle Daily Words",
    )
    grp.add_argument(
        "--wordle",
        action="store_const",
        const=(lexicons.wordle.lexicon,) * 2,
        dest="solution_space",
        help="Wordle. This is the default.",
    )
    grp.add_argument(
        "--wordle-6",
        action="store_const",
        const=(lexicons.wordle_6.lexicon,) * 2,
        dest="solution_space",
        help="6 Letter Wordle",
    )
    grp.add_argument(
        "--primes",
        action="store_const",
        const=(lexicons.primes.primes,) * 2,
        dest="solution_space",
        help="5 digit primes",
    )
    grp.add_argument(
        "--nerdle",
        action="store_const",
        const=(lexicons.nerdle.columns_8,) * 2,
        dest="solution_space",
        help="Nerdle",
    )
    grp.add_argument(
        "--mini-nerdle",
        action="store_const",
        const=(lexicons.nerdle.columns_6,) * 2,
        dest="solution_space",
        help="Mini Nerdle",
    )
    parser.set_defaults(lexicon=(lexicons.wordle.lexicon,) * 2)
    args = parser.parse_args()
    lexicon, candidates = args.solution_space
    main(
        lexicon,
        candidates,
        args.hard_mode,
        args.random,
        args.regexp,
    )
