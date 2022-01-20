import itertools

CORRECT = "2"
PRESENT = "1"
ABSENT = "0"

_collector = {
    t: "".join(t)
    for t in itertools.product(
        (ABSENT, PRESENT, CORRECT),
        repeat=5,
    )
}


def matches(target, guess):
    target_list = list(target)
    guess_list = list(guess)
    res = [""] * 5

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
    return _collector[tuple(res)]


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
