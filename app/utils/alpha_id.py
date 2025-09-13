# app/utils/alpha_id.py
from pathlib import Path
import re

NOTES_DIR = Path("data/notes")

def _to_num(s: str, order="A"):  # "A" = aaab; "B" = baaa
    base = 26
    s = s.lower()
    if order == "A":  # a a a a -> last char least significant
        acc = 0
        for c in s:
            acc = acc * base + (ord(c) - 97)
        return acc
    else:  # order "B": first char least significant (aaaa -> baaa)
        acc, mul = 0, 1
        for c in s:
            acc += (ord(c) - 97) * mul
            mul *= base
        return acc

def _from_num(n: int, order="A"):
    base = 26
    chars = ['a','a','a','a']
    if order == "A":
        for i in range(3, -1, -1):
            chars[i] = chr(97 + (n % base))
            n //= base
    else:
        for i in range(0, 4):
            chars[i] = chr(97 + (n % base))
            n //= base
    return "".join(chars)

def next_alpha_id(order="A"):
    pattern = re.compile(r"([a-z]{4})\.json$", re.I)
    max_n = -1
    for f in NOTES_DIR.glob("*.json"):
        m = pattern.match(f.name)
        if m:
            n = _to_num(m.group(1), order)
            max_n = max(max_n, n)
    return _from_num(max_n + 1 if max_n >= 0 else 0, order)
