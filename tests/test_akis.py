"""Üreteçler, boru hattı ve rota sayacı testleri."""

from itertools import islice, takewhile

import pytest

from uzay_oyunu.akis import fibonacci, yakit_gostergesi
from uzay_oyunu.oyun import travel


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


# --- Görev 2: Yakıt göstergesi ---

def test_yakit_gostergesi():
    assert list(yakit_gostergesi(100, 30)) == [70, 40, 10, 0]


def test_yakit_gostergesi_stopiteration():
    gosterge = yakit_gostergesi(10, 5)
    assert next(gosterge) == 5
    assert next(gosterge) == 0
    with pytest.raises(StopIteration):
        next(gosterge)


def test_travel_yakit_bitince_oyun_biter(monkeypatch, capsys):
    # dünya <-> centauri arasında hep [1] seçilir; 100/5 = 20 yolculuktan sonra yakıt biter.
    monkeypatch.setattr("builtins.input", lambda _: "1")
    travel()
    cikti = capsys.readouterr().out
    assert "Kalan yakıt: 0" in cikti
    assert cikti.rstrip().endswith("Yakıtın bitti, uzayda sürükleniyorsun…")
