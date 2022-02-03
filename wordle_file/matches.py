import functools

CORRECT = "2"
PRESENT = "1"
ABSENT = "0"


@functools.cache
def _collect(t):
    return "".join(t)


def matches(target, guess):
    target_list = list(target)
    guess_list = list(guess)
    res = [""] * len(guess)

    for i, c in enumerate(guess):
        if target_list[i] == c:
            target_list[i] = None
            guess_list[i] = None
            res[i] = CORRECT

    for i, c in enumerate(guess_list):
        if c is not None:
            try:
                target_list[target_list.index(c)] = None
            except ValueError:
                res[i] = ABSENT
            else:
                res[i] = PRESENT
    return _collect(tuple(res))


def matches_table(guesses, targets):
    return (
        [
            matches(
                guess=wa,
                target=wb,
            )
            for wb in targets
        ]
        for wa in guesses
    )
