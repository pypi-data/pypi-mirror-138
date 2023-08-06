
from typing import TypeVar, List, Any
from functools import reduce
import textwrap

T = TypeVar("T")

def wrap(txt: str) -> str:
    return ["\n".join(textwrap.wrap(l, width = 72)) for l in txt.split("\n")]

def deduplicate(l: List[Any])-> List[T]:
    def _dup(a,b):
        if len(a) == 0:
            return [b]
        elif a[-1] == b:
            return a
        else:
            return a + [b]

    return reduce(_dup, l, [])

def process(text):
    return "\n".join(deduplicate(wrap(text)))
