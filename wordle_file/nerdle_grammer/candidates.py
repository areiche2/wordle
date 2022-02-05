import argparse
import itertools


def ndigit(n, zero_allowed=False):
    if n == 1:
        yield from "123456789"
        if zero_allowed:
            yield "0"
        return
    for ld in "123456789":
        for rem in itertools.product("0123456789", repeat=n - 1):
            yield ld + "".join(rem)


def irange(start, stop):
    return range(start, stop + 1)


def lhs(n):
    # First number must leave two characters for operand
    # and one more character
    for i in irange(1, n - 2):
        for num in ndigit(i):
            yield from lhs_rec(n - i, [num])
            # yield from lhs_rec(n - i - 1, ["-" + num])


def lhs_rec(n, body):
    if n == 0:
        yield "".join(body)
        return
    if n == 1:
        # Need two or more characters
        return
    for op in "+-*/":
        for i in irange(1, n - 1):
            for num in ndigit(i):
                yield from lhs_rec(n - 1 - i, body + [op, num])


def eqs(n):
    # n = number of columns
    # LHS: Must have at least two numbers and operand
    # At least two characters for RHS
    for n_lhs in irange(3, n - 2):
        for s in lhs(n_lhs):
            try:
                val = eval(s)
            except ZeroDivisionError:
                pass
            else:
                if isinstance(val, int) or val.is_integer():
                    val = int(val)
                    if len(str(val)) + len(s) + 1 == n:
                        yield f"{s}={val}", val


def main(n):
    for e, v in eqs(n):
        if v >= 0:
            print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Candidates for Nerdle")
    parser.add_argument(
        "--n",
        type=int,
        action="store",
        default=6,
        help="Number of columns",
    )
    main(parser.parse_args().n)
