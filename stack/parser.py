from __future__ import annotations

from collections.abc import Iterable

from stack import tokenizer
from stack.excs import ParserError
from stack.expr import Expression
from stack.expr import Lambda
from stack.expr import Literal
from stack.tokenizer import Token

SWAP = Expression("SWAP")
DUP = Expression("DUP")
DROP = Expression("DROP")
APPLY = Expression("APPLY")

LOAD = Expression("LOAD")
STORE = Expression("STORE")

ADD = Expression("+")
SUB = Expression("-")
MUL = Expression("*")

EQUALS = Expression("=")
LESS_THAN = Expression("<")
GREATER_THAN = Expression(">")

NOT = Expression("!")
AND = Expression("&")
OR = Expression("|")
XOR = Expression("^")


TOKEN_MAP = {
    tokenizer.SWAP: SWAP,
    tokenizer.DUP: DUP,
    tokenizer.DROP: DROP,
    tokenizer.APPLY: APPLY,
    # store/load
    tokenizer.LOAD: LOAD,
    tokenizer.STORE: STORE,
    # arithmetic
    tokenizer.ADD: ADD,
    tokenizer.SUB: SUB,
    tokenizer.MUL: MUL,
    # comparison
    tokenizer.EQUALS: EQUALS,
    tokenizer.LESS_THAN: LESS_THAN,
    tokenizer.GREATER_THAN: GREATER_THAN,
    # logic
    tokenizer.NOT: NOT,
    tokenizer.AND: AND,
    tokenizer.OR: OR,
    tokenizer.XOR: XOR,
}


def parse(tokens: Iterable[Token]) -> Iterable[Expression]:
    expr_stack: list[Expression | None] = []

    for token in tokens:
        if token is tokenizer.L_BRACKET:
            expr_stack.append(None)
        elif token is tokenizer.R_BRACKET:
            if not expr_stack:
                raise ParserError("Unmatched right bracket")

            nested: list[Expression] = []
            while True:
                expr = expr_stack.pop()
                if expr is None:
                    break
                nested.append(expr)

            nested.reverse()
            yield Lambda(nested)

        else:
            if isinstance(token, tokenizer.Literal):
                expr = Literal(token.value)
            else:
                expr = TOKEN_MAP[token]

            if expr_stack:
                expr_stack.append(expr)
            else:
                yield expr

    if expr_stack:
        raise ParserError("Unmatched left bracket")
