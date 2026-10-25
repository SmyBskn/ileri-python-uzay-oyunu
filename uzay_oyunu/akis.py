"""Hafta 4 yönergesindeki üreteçler ve rota hesabı."""

from typing import Iterator


def fibonacci() -> Iterator[int]:
    """Sonsuz Fibonacci sayılarını sırayla üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki


def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    """Her adımda yakıt tüketip kalan yakıtı üretir; sıfırdan sonra durur."""
    if tuketim <= 0:
        raise ValueError("tuketim pozitif olmalıdır")
    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit
