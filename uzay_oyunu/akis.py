"""Hafta 4 yönergesindeki üreteçler ve rota hesabı."""

from typing import Iterator


def fibonacci() -> Iterator[int]:
    """Sonsuz Fibonacci sayılarını sırayla üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki
