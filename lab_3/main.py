import re
import csv

from json import load


def validate(s: list[str], patterns: dict[str, str]) -> bool:
    for val, pattern in zip(s, patterns.values()):
        if not re.match(pattern, val):
            return False
    return True

def process_data(path_to_patterns: str, path_to_data: str) -> list[int]:
    with open(path_to_patterns, mode="r", encoding="utf-8") as f:
        patterns: dict[str, str] = load(f)

    res: list[int] = []

    lines: list[list[str]] = []
    with open(path_to_data, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                lines.append(row)

    for num, line in enumerate(lines[1:]):
        if not validate(line, patterns):
            res.append(num - 2)

    return res
