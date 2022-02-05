import argparse
import itertools
import json
import re


def get_response(n):
    while True:
        resp = input("\t* Response (enter to quit): ")
        if len(resp) == n and re.fullmatch("[012]+", resp):
            return resp
        print("\t* Not recognized.")


def main(src):
    print("Responses: absent = 0, present = 1, correct = 2")
    trans = str.maketrans("012", "⬛🟨🟩")
    node = json.load(src)
    for i in itertools.count(start=1):
        print(f"# Round {i}")
        candidates = node["candidates"]
        print(f"\t* Candidates: {len(candidates)}")
        print(*(f"\t\t* {c}" for c in candidates[:5]), sep="\n")
        if len(candidates) > 5:
            print("\t\t* ...")
        print(f"\t* Guess {node['guess']}")
        if len(candidates) == 1:
            return
        while True:
            resp = get_response(len(node["guess"]))
            if not resp or re.fullmatch("2+", resp):
                print("\t* Solved")
                return
            if resp in node["response"]:
                break
            print(f"\t* {resp.translate(trans)} not found. Please try again.")

        node = node["response"][resp]


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Wordle Solver")
    parser.add_argument(
        "json",
        type=argparse.FileType("r"),
        help="JSON file with responses",
    )
    main(parser.parse_args().json)
