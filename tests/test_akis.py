"""Üreteçler, boru hattı ve rota sayacı testleri."""

from itertools import islice, takewhile
from pathlib import Path
from types import GeneratorType

import pytest

from uzay_oyunu.akis import (
    ayristir,
    fibonacci,
    rota_sayaci,
    satirlari_oku,
    uzun_yolculuklar,
    yakit_gostergesi,
    zamanlayici,
)
from uzay_oyunu.galaksi import galaksi_kur
from uzay_oyunu.oyun import travel

SEYIR = str(Path(__file__).resolve().parent.parent / "veri" / "seyir.txt")


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


# --- Görev 3: Seyir defteri boru hattı ---

def test_seyir_toplam_yakit():
    assert sum(y for _, _, y in ayristir(satirlari_oku(SEYIR))) == 88


def test_seyir_uzun_yolculuklar():
    kayitlar = ayristir(satirlari_oku(SEYIR))
    assert [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)] == [
        "sirius", "centauri", "orion", "kara_delik"
    ]


def test_boru_hatti_tembel():
    # Hiçbir aşama liste döndürmez; hepsi üreteçtir.
    satirlar = satirlari_oku(SEYIR)
    kayitlar = ayristir(satirlar)
    uzunlar = uzun_yolculuklar(kayitlar, 10)
    assert all(isinstance(a, GeneratorType) for a in (satirlar, kayitlar, uzunlar))
    assert next(uzunlar) == ("dünya", "sirius", 12)


def test_satirlari_oku_yorum_ve_bos_satirlari_atlar():
    satirlar = list(satirlari_oku(SEYIR))
    assert len(satirlar) == 6
    assert not any(s.startswith("#") or not s for s in satirlar)


# --- Görev 4: Önbellekli rota sayacı ---

def test_rota_sayaci_ornek_degerler():
    say = rota_sayaci(galaksi_kur()["baglantilar"])
    assert (say("dünya", 3), say("dünya", 10), say("dünya", 40)) == (9, 2185, 16832258606399)


def test_rota_sayaci_onbellek_kullanir():
    say = rota_sayaci(galaksi_kur()["baglantilar"])
    say("dünya", 20)
    bilgi = say.cache_info()
    assert bilgi.hits > 0
    assert bilgi.currsize <= 5 * 21  # en fazla (gezegen, adim) çifti kadar


# --- Bonus: zamanlayıcı ---

def test_zamanlayici_aralik_dolmadan_false():
    z = zamanlayici(60)
    assert next(z) is False
