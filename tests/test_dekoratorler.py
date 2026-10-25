"""Hafta 5 dekoratör testleri."""

from ornekler import fibonacci_sayaclari
from uzay_oyunu.dekoratorler import say, sure_olc


def test_sure_olc_sonucu_korur(capsys):
    @sure_olc
    def topla(a, b):
        """İki sayıyı toplar."""
        return a + b
    assert topla(2, 4) == 6
    assert "topla:" in capsys.readouterr().out


def test_sure_olc_adli_argumanlar():
    @sure_olc
    def carp(a, *, b):
        return a * b
    assert carp(3, b=5) == 15


def test_sure_olc_name_doc_korur():
    def ornek(x):
        """Örnek belge."""
        return x
    sarilmis = sure_olc(ornek)
    assert sarilmis.__name__ == "ornek"
    assert sarilmis.__doc__ == "Örnek belge."


def test_say_cagri_sayar():
    @say
    def iki_kat(x):
        return 2 * x
    assert iki_kat(3) == 6
    assert iki_kat(4) == 8
    assert iki_kat.cagri == 2


def test_fib_dekorator_sirasi():
    assert fibonacci_sayaclari() == (21891, 39, 21)


def test_yardimci_dekoratorlar_wraps():
    @say
    def ornek():
        """belge"""
        return 1
    assert ornek.__name__ == "ornek"
    assert ornek.__doc__ == "belge"
