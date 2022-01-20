import itertools
import re

import heuristic_guess
import lexicon
import matches

FIRST_GUESS = "serai"


def get_response():
    while True:
        resp = input("* Response: ")
        if re.fullmatch("[012]{5}", resp):
            return resp


def main(is_hard_mode, daily_only):
    print(
        f"absent = {matches.ABSENT}, present = {matches.PRESENT},"
        f" correct={matches.CORRECT}"
    )
    guess = FIRST_GUESS
    candidates = lexicon.daily_words[:] if daily_only else lexicon.lexicon[:]
    for i in itertools.count(start=1):
        print(f"# Round {i}")
        print(f"* Guess {guess}")
        resp = get_response()
        if resp == "22222":
            print("\t* Solved")
            break
        candidates = tuple(
            filter(
                lambda s: resp == matches.matches(s, guess),
                candidates,
            )
        )
        print(f"* Number of Candidates: {len(candidates)}")
        print(*(f"\t* {c}" for c in candidates[:10]), sep="\n")
        if len(candidates) > 10:
            print("\t* ...")
        if not candidates:
            print(
                "ERROR: Zero candidates. Did you type in a response incorrectly?",  # noqa: E501
            )
            break
        if len(candidates) == 1:
            print(f"* Guess {candidates[0]} to solve")
            break
        guess = heuristic_guess.guess(
            guesses=candidates if is_hard_mode else lexicon.lexicon,
            targets=candidates,
        )


if __name__ == "__main__":
    main(False, True)
