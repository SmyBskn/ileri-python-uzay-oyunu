"""Komut sistemi testleri."""

import pytest

from uzay_oyunu.galaksi import galaksi_kur
from uzay_oyunu.komutlar import KOMUTLAR, envanter, harita, komut, yardim
from uzay_oyunu.oyun import travel


def test_yardim_komutu():
    assert yardim(galaksi_kur()) == (
        "envanter eşyalarını gösterir\n"
        "harita gidebileceğin gezegenleri gösterir\n"
        "yardim komutları listeler"
    )


def test_envanter_komutu():
    sonuc = envanter(galaksi_kur())
    assert "standart motor" in sonuc
    assert "Kredi: 100" in sonuc


def test_harita_komutu():
    durum = galaksi_kur()
    assert harita(durum) == "centauri, sirius"
    durum["konum"] = "sirius"
    assert harita(durum) == "orion, dünya, kara_delik"


def test_komutlar_kayitli_ve_degismemis():
    # Kayıt deseni fonksiyonu sarmalamaz; sözlükteki nesne fonksiyonun kendisidir.
    assert KOMUTLAR["yardim"] == (yardim, "komutları listeler")
    assert KOMUTLAR["harita"][0] is harita
    assert KOMUTLAR["envanter"][0] is envanter


def test_komut_dekoratoru_ayni_adi_reddeder():
    ad = "test_cakisma"
    try:
        @komut(ad, "test")
        def birinci(durum):
            return "bir"
        with pytest.raises(ValueError):
            @komut(ad, "tekrar")
            def ikinci(durum):
                return "iki"
    finally:
        KOMUTLAR.pop(ad, None)


def test_travel_komutu_calistirir_ve_menuyu_tekrar_gosterir(monkeypatch, capsys):
    # dünya'dan sirius'a git, harita komutu yaz; ardından girdi bitince oyunu kes.
    girdiler = iter(["2", "harita"])

    def sahte_input(_):
        try:
            return next(girdiler)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", sahte_input)
    with pytest.raises(EOFError):
        travel()
    cikti = capsys.readouterr().out
    assert "sirius gezegenine ulaştın" in cikti
    assert "orion, dünya, kara_delik" in cikti
    # Komuttan sonra aynı sirius menüsü yeniden gösterilir. (Gerçek satır sonlarıyla
    # arıyoruz; log_cagri satırındaki repr'de satır sonları \n olarak yazılır.)
    sirius_menusu = "Nereye gitmek istersin?\n[1] orion\n[2] dünya\n[3] kara_delik"
    assert cikti.count(sirius_menusu) == 2
