"""Galaksi verisi üzerinde map/filter/reduce ve partial örnekleri."""

from functools import partial, reduce

from uzay_oyunu.galaksi import galaksi_kur
from uzay_oyunu.oyun import yolculuk


def gezegen_adlari(baglantilar: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    """Gezegen adlarının büyük harfli listesini iki yöntemle döndürür."""
    birinci = list(map(str.upper, baglantilar.keys()))
    ikinci = [ad.upper() for ad in baglantilar]
    return birinci, ikinci


def cok_baglantili(baglantilar: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    """En az iki bağlantısı olan gezegenleri iki yöntemle döndürür."""
    birinci = list(map(
        lambda oge: oge[0],
        filter(lambda oge: len(oge[1]) >= 2, baglantilar.items())
    ))
    ikinci = [ad for ad, komsular in baglantilar.items() if len(komsular) >= 2]
    return birinci, ikinci


def toplam_baglanti(baglantilar: dict[str, list[str]]) -> tuple[int, int]:
    """Toplam bağlantı sayısını reduce ve sum ile hesaplar."""
    birinci = reduce(lambda toplam, komsular: toplam + len(komsular), baglantilar.values(), 0)
    ikinci = sum(len(komsular) for komsular in baglantilar.values())
    return birinci, ikinci


# Okunaklılık: liste üreteci ve sum daha okunaklı; soldan sağa bir cümle gibi
# okunuyor. map/filter ile lambda iç içe girince ne döndüğünü anlamak için
# ifadeyi içten dışa çözmek gerekiyor; reduce ise toplamı gizliyor.
# map(str.upper, ...) gibi hazır bir fonksiyon verilince map de kısa ve açık.

hizli_yolculuk = partial(yolculuk, hiz=3)


if __name__ == "__main__":
    baglantilar = galaksi_kur()["baglantilar"]
    print(gezegen_adlari(baglantilar)[0])
    print(cok_baglantili(baglantilar)[0])
    print(toplam_baglanti(baglantilar)[0])
    print(hizli_yolculuk("orion"))
