import datetime
import hashlib
import urllib.error
import urllib.parse
import urllib.request

URL = "https://www.nerdlegame.com"
# Code use 1642636800
ORIGIN_DATE = datetime.date(2022, 1, 21)


def translate(x, shift, bound):
    return (x + shift) % bound if x < bound else x


def decode(s):
    return "".join(chr(translate(o, -13, 126)) for o in (ord(c) for c in s))


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
        str(datetime.timedelta(days=i) + ORIGIN_DATE),
        req("words", offset),
        req("miniwords", offset),
    )


for i in range(1, 17000):
    print(*row(i), sep="\t")
