from __future__ import annotations

from typing import TypeGuard

from stack.excs import InterpreterError
from stack.expr import Expression
from stack.expr import Lambda
from stack.expr import Literal


def is_literal(t: Expression) -> TypeGuard[Literal]:
    if not isinstance(t, Literal):
        raise InterpreterError(f"Expected literal, got {t}")
    return True


def op_SWAP(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()
    stack.append(a)
    stack.append(b)


def op_DUP(stack: list[Expression]) -> None:
    a = stack.pop()
    stack.append(a)
    stack.append(a)


def op_DROP(stack: list[Expression]) -> None:
    stack.pop()


def op_APPLY(stack: list[Expression]) -> list[Expression]:
    a = stack.pop()

    if isinstance(a, Lambda):
        return a.nested.copy()
    else:
        return [a]


# store/load
def op_LOAD(stack: list[Expression], registry: dict[int, Expression]) -> None:
    a = stack.pop()

    assert is_literal(a)

    val = registry.get(a.value)
    if val is None:
        return
    stack.append(val)


def op_STORE(stack: list[Expression], registry: dict[int, Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a)
    registry[a.value] = b


# binary operators
def op_ADD(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(a.value + b.value))


def op_SUB(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(a.value - b.value))


def op_MUL(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(a.value * b.value))


# comparison operators
def op_EQUALS(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(int(a.value == b.value)))


def op_LESS_THAN(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(int(a.value < b.value)))


def op_GREATER_THAN(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(int(a.value > b.value)))


# boolean operators
def op_NOT(stack: list[Expression]) -> None:
    a = stack.pop()

    assert is_literal(a)
    stack.append(Literal(int(not a.value)))


def op_AND(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(int(a.value and b.value)))


def op_OR(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(int(a.value or b.value)))


def op_XOR(stack: list[Expression]) -> None:
    a = stack.pop()
    b = stack.pop()

    assert is_literal(a) and is_literal(b)
    stack.append(Literal(int(bool(a.value) ^ bool(b.value))))
