from __future__ import annotations

from typing import TextIO

from stack import interpreter
from stack import parser
from stack import tokenizer

MAX_EXPR = 2048


def run(src: TextIO) -> int:
    tokens = tokenizer.tokenize(src)
    exprs = parser.parse(tokens)
    stack = interpreter.interpret(exprs, max_counter=MAX_EXPR)

    print(" ".join(repr(expr) for expr in stack))

    return 0
