import argparse
import collections
import json
import random
import re

import heuristic_guess
import lexicon
import matches


def expand_graph(is_hard_mode, candidates, is_random, depth):
    if not candidates:
        raise ValueError("Error: No candidates.")
    if len(candidates) == 1:
        return {
            "guess": candidates[0],
            "response": {},
            "depth": depth,
            "candidates": candidates,
        }
    guesses = candidates if is_hard_mode else lexicon.lexicon
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
            resp: expand_graph(is_hard_mode, grp, is_random, depth + 1)
            for resp, grp in gather.items()
            if resp != "22222"
        },
        "depth": depth,
        "candidates": sorted(candidates),
    }


def main(is_hard_mode, is_resticted, is_random, regexp):
    initial_set = lexicon.daily_words if is_resticted else lexicon.lexicon
    if regexp:
        initial_set = [w for w in initial_set if re.search(regexp, w)]
    res = expand_graph(is_hard_mode, initial_set, is_random, 0)
    print(json.dumps(res))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Wordle File Generator")
    parser.add_argument(
        "--hard-mode",
        action="store_true",
        help="JSON file with responses",
    )
    parser.add_argument(
        "--restricted",
        action="store_true",
        help="Assume word from solution set",
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
    args = parser.parse_args()
    main(args.hard_mode, args.restricted, args.random, args.regexp)
