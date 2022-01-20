import argparse
import collections
import json

import heuristic_guess
import lexicon
import matches


def expand_graph(is_hard_mode, candidates, depth):
    if not candidates:
        raise ValueError("Error: No candidates.")
    if len(candidates) == 1:
        return {
            "guess": candidates[0],
            "response": {},
            "depth": depth,
            "candidates": candidates,
        }
    guess = heuristic_guess.guess(
        guesses=candidates if is_hard_mode else lexicon.lexicon,
        targets=candidates,
    )
    gather = collections.defaultdict(list)
    for c in candidates:
        gather[matches.matches(target=c, guess=guess)].append(c)
    return {
        "guess": guess,
        "response": {
            resp: expand_graph(is_hard_mode, grp, depth + 1)
            for resp, grp in gather.items()
            if resp != "22222"
        },
        "depth": depth,
        "candidates": candidates,
    }


def main(is_hard_mode, is_resticted):
    initial_set = lexicon.daily_words if is_resticted else lexicon.lexicon
    res = expand_graph(is_hard_mode, initial_set, 0)
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
    args = parser.parse_args()
    main(args.hard_mode, args.restricted)
