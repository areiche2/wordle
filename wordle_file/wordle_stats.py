import argparse
import collections
import itertools
import json

import lexicon
import matches


def simulate(node, target):
    for i in itertools.count(start=1):
        resp = matches.matches(target=target, guess=node["guess"])
        if resp == "22222":
            return i
        if resp is None or resp not in node["response"]:
            break
        node = node["response"][resp]
    return -1


def main(src):
    node = json.load(src)
    res = list(
        filter(
            lambda x: x[1] != -1,
            ((w, simulate(node, w)) for w in lexicon.lexicon),
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Wordle Solver")
    parser.add_argument(
        "json",
        type=argparse.FileType("r"),
        help="JSON file with responses",
    )
    main(parser.parse_args().json)
