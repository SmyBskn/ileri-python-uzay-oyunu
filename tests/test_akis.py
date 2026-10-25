"""Üreteçler, boru hattı ve rota sayacı testleri."""

from itertools import islice, takewhile

from uzay_oyunu.akis import fibonacci


# --- Görev 1: Fibonacci ---

def test_fibonacci_next_ile_ilk_uc():
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice_ve_takewhile():
    assert list(islice(fibonacci(), 12)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert list(takewhile(lambda n: n < 100, fibonacci())) == [
        0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
    ]


def test_fibonacci_ureteci_tek_kullanimlik():
    g = fibonacci()
    ilk = list(islice(g, 12))
    ikinci = list(islice(g, 12))
    assert ilk != ikinci
    assert ikinci[0] == 144  # kaldığı yerden devam eder
