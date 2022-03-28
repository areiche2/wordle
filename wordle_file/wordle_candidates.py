import argparse
import itertools
import re

import lexicons
import matches


def get_response(message, check_resp):
    while True:
        resp = input(f"\t* {message} (enter to quit): ")
        if not resp:
            return None
        if check_resp(resp):
            return resp
        print("\t* Not recognized.")


def main(
    lexicon,
    candidates,
):
    n = len(lexicon[0])
    lexicon = set(lexicon)
    for i in itertools.count(start=1):
        print(f"# Round {i}")
        print(f"\t* Candidates: {len(candidates)}")
        print(*(f"\t\t* {c}" for c in candidates[:5]), sep="\n")
        if len(candidates) > 5:
            print("\t\t* ...")
        if len(candidates) == 1:
            print(f"* Guess {candidates[0]}")
            return
        guess = get_response("Guess", lambda s: s in lexicon)
        if not guess:
            return
        resp = get_response(
            "Response",
            lambda s: re.fullmatch(f"[012]{{{n}}}", s),
        )
        if not resp:
            return
        candidates = list(
            filter(
                lambda s: matches.matches(target=s, guess=guess) == resp,
                candidates,
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Wordle Iterative: Lists candidates")
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
    parser.set_defaults(solution_space=(lexicons.wordle.lexicon,) * 2)
    args = parser.parse_args()
    parser.set_defaults(solution_space=(lexicons.wordle.lexicon,) * 2)
    lexicon, candidates = args.solution_space
    main(
        lexicon,
        candidates,
    )
