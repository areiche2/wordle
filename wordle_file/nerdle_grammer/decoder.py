import datetime
import hashlib
import urllib.error
import urllib.parse
import urllib.request

URL = "https://www.nerdlegame.com"
# Code use 1642636800
# Dates are UTC
ORIGIN_DATE = datetime.date(2022, 1, 20)


def translate(x, shift, bound):
    return (x + shift) % bound if x < bound else x


def decode(s):
    return "".join(chr(translate(ord(c), -13, 126)) for c in s)


def hash(n):
    return hashlib.md5(str(n).encode("utf-8")).hexdigest()


def req(path, offset):
    url = urllib.parse.urljoin(URL, f"{path}/{hash(offset)}")
    try:
        with urllib.request.urlopen(url) as response:
            return decode(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return f"[{e.code}]"


def row(offset):
    return (
        offset,
        hash(offset),
        str(datetime.timedelta(days=offset) + ORIGIN_DATE),
        req("words", offset),
        req("miniwords", offset),
    )


def main(n):
    for i in range(n):
        print(*row(i), sep="\t")


if __name__ == "__main__":
    main(500)
