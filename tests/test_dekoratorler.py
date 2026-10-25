"""Hafta 5 dekoratör testleri."""

from uzay_oyunu.dekoratorler import sure_olc


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
