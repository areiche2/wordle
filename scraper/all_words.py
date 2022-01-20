import json

from words import other_words, starting_words

print(
    json.dumps(
        sorted(list(set(starting_words + other_words))),
        indent=4,
    )
)
