"""İstatistik yardımcı fonksiyonları testleri."""

from functools import partial

from istatistik import cok_baglantili, gezegen_adlari, hizli_yolculuk, toplam_baglanti
from uzay_oyunu.galaksi import galaksi_kur


def test_gezegen_adlari():
    birinci, ikinci = gezegen_adlari(galaksi_kur()["baglantilar"])
    assert birinci == ikinci == ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]


def test_cok_baglantili():
    birinci, ikinci = cok_baglantili(galaksi_kur()["baglantilar"])
    assert birinci == ikinci == ["dünya", "centauri", "sirius", "orion"]


def test_toplam_baglanti():
    birinci, ikinci = toplam_baglanti(galaksi_kur()["baglantilar"])
    assert birinci == ikinci == 10


def test_partial_hizli_yolculuk():
    assert isinstance(hizli_yolculuk, partial)
    assert hizli_yolculuk.keywords == {"hiz": 3}
    assert hizli_yolculuk("orion") == "orion hiz=3"
