from datetime import date, timedelta
from words import starting_words
orig = date(2021,6,19)
for i in range(len(starting_words)):
    print(i, orig+timedelta(days=i), starting_words[i], sep="\t")
