import argparse
import collections
import os
import urllib.error
import urllib.parse
import urllib.request


def cannonical(s):
    return tuple(sorted(s))


def solution_map():
    soln = collections.defaultdict(list)
    dirname = os.path.dirname(__file__)
    for line in open(os.path.join(dirname, "data/cols8.txt")):
        p = line.strip()
        soln[cannonical(p)].append(p)
    return soln


def fetch(challange):
    url = f"https://api.nerdlegame.com/decode/decryptSolution?encoded={challange}"
    with urllib.request.urlopen(url) as response:
        res = response.read().decode("utf-8").split("_")
        return res[0], int(res[1]) - 1


def matches_at_n(eqn, candidate, n):
    return eqn[n] == candidate[n]


def main(challange):
    soln = solution_map()
    try:
        puzzle, n = fetch(challange)
    except urllib.error.HTTPError as e:
        print(f"Failed with error {e.code}")
    else:
        matches = soln.get(cannonical(puzzle))
        if matches:
            for candidate in matches:
                if matches_at_n(candidate, puzzle, n):
                    print(candidate)
            return
        print("Nothing Found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Wordle File Generator")
    parser.add_argument(
        "challange",
        action="store",
        help="URL hash",
    )
    main(parser.parse_args().challange)
