import itertools
import json


def ndigit(n):
    if n == 1:
        yield from "0123456789"
        return
    for ld in "123456789":
        for rem in itertools.product("0123456789", repeat=n - 1):
            yield ld + "".join(rem)


def lhs(n):
    for i in range(1, n + 1):
        for num in ndigit(i):
            yield from lhs_rec(n - i, [num])
            # yield from lhs_rec(n - i - 1, ["-" + num])


def lhs_rec(n, body):
    if n < 0:
        return
    if n == 0:
        yield "".join(body)
    for op in "+-*/":
        for i in range(1, n):
            for num in ndigit(i):
                yield from lhs_rec(n - 1 - i, body + [op, num])


def eqs(n):
    for n_lhs in range(1, n - 1):
        for s in lhs(n_lhs):
            try:
                val = eval(s)
            except ZeroDivisionError:
                pass
            else:
                if isinstance(val, int) or val.is_integer():
                    val = str(int(val))
                    if len(val) + len(s) + 1 == n:
                        yield f"{s}={val}"


def main(n):
    res = list(eqs(n))
    print(json.dumps(res, indent=4))


if __name__ == "__main__":
    main(6)
