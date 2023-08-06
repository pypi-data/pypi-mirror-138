from typing import Iterator


def concat_iterators(x: Iterator, y: Iterator) -> Iterator:
    yield from x
    yield from y
