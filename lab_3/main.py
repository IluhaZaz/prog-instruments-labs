import re
import csv

from json import load


with open("patterns.json", mode="r", encoding="utf-8") as f:
    patterns = load(f)

def validate(s: list[str], patterns: dict[str, str]):
    for val, pattern in zip(s, patterns.values()):
        if not re.match(pattern, val):
            print(val)
            return False
    return True

res = []

lines = []
with open("36.csv", mode="r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            lines.append(row)

for num, line in enumerate(lines[1:]):
    if not validate(line, patterns):
        res.append(num - 2)
print(len(res))
        


