import argparse
import collections
import itertools
import json
import re

import matches


def simulate(node, target):
    res = []
    for i in itertools.count(start=1):
        guess = node["guess"]
        resp = matches.matches(target=target, guess=guess)
        res.append((guess, resp, len(node["candidates"])))
        if re.fullmatch("2+", resp):
            return res
        node = node["response"][resp]
    return []


def stats(node):
    candidates = node["candidates"]
    res = list(
        filter(
            lambda x: x[1] > 0,
            ((w, len(simulate(node, w))) for w in candidates),
        )
    )
    tot = sum(s[1] for s in res)
    print("words:", len(res), sep="\t")
    print("guess:", tot, sep="\t")
    print("avg:", tot / len(res), sep="\t")
    agg = collections.defaultdict(list)
    for w, c in res:
        agg[c].append(w)
    for w, g in sorted(agg.items()):
        print(w, len(g), *g[:5], sep="\t")


def single_word(node, word):
    if word not in node["candidates"]:
        print("Word not in solution set.")
        return
    res = simulate(node, word)
    trans = str.maketrans("012", "⬛🟨🟩")
    for w, g, n in res:
        print(w, g.translate(trans), n, sep="\t")


def main(src, word):
    node = json.load(src)
    if word:
        single_word(node, word)
    else:
        stats(node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Wordle Solver")
    parser.add_argument(
        "json",
        type=argparse.FileType("r"),
        help="JSON file with responses",
    )
    parser.add_argument(
        "--word",
        type=str,
        help="Evaluate a single word",
    )
    args = parser.parse_args()
    main(args.json, args.word)
