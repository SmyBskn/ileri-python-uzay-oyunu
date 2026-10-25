"""Hafta 5 dekoratör testleri."""

from ornekler import fibonacci_sayaclari
from uzay_oyunu.dekoratorler import log_cagri, say, sure_olc
from uzay_oyunu.galaksi import galaksi_kur
from uzay_oyunu.oyun import hedef_menusu, yolculuk


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


def test_log_cagri(capsys):
    @log_cagri
    def selam(ad, *, resmi=False):
        return f"Merhaba {ad}, resmi={resmi}"
    assert selam("Ada", resmi=True) == "Merhaba Ada, resmi=True"
    cikti = capsys.readouterr().out
    assert "-> selam('Ada', resmi=True)" in cikti
    assert "<- selam =" in cikti


def test_log_cagri_ornek_cikti(capsys):
    assert log_cagri(yolculuk)("orion", hiz=3) == "orion hiz=3"
    assert capsys.readouterr().out == (
        "-> yolculuk('orion', hiz=3)\n"
        "<- yolculuk = 'orion hiz=3'\n"
    )


def test_log_cagri_oyun_fonksiyonlarini_bozmaz(capsys):
    assert galaksi_kur.__name__ == "galaksi_kur"
    assert hedef_menusu.__name__ == "hedef_menusu"
    assert galaksi_kur()["konum"] == "dünya"
    assert hedef_menusu(["orion", "sirius"]) == "Nereye gitmek istersin?\n[1] orion\n[2] sirius"
    cikti = capsys.readouterr().out
    assert "-> galaksi_kur()" in cikti
    assert "-> hedef_menusu(['orion', 'sirius'])" in cikti


def test_fib_dekorator_sirasi():
    assert fibonacci_sayaclari() == (21891, 39, 21)


def test_yardimci_dekoratorlar_wraps():
    @say
    def ornek():
        """belge"""
        return 1
    assert ornek.__name__ == "ornek"
    assert ornek.__doc__ == "belge"
