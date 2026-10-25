"""Hafta 4 rota ölçümünü ve Hafta 5 dekoratör örneklerini çalıştırır.

Çalıştırma: uv run python ornekler.py
"""

from time import perf_counter

from uzay_oyunu.akis import rota_sayaci, rota_sayaci_onbelleksiz
from uzay_oyunu.dekoratorler import sure_olc
from uzay_oyunu.galaksi import galaksi_kur


def rota_olcumleri(adim: int = 20) -> None:
    """Önbelleksiz ve önbellekli rota sayacını perf_counter ile karşılaştırır."""
    baglantilar = galaksi_kur()["baglantilar"]

    onbelleksiz = rota_sayaci_onbelleksiz(baglantilar)
    baslangic = perf_counter()
    sonuc1 = onbelleksiz("dünya", adim)
    sure1 = perf_counter() - baslangic

    onbellekli = rota_sayaci(baglantilar)
    baslangic = perf_counter()
    sonuc2 = onbellekli("dünya", adim)
    sure2 = perf_counter() - baslangic

    print(f"Önbelleksiz adim={adim}: {sure1:.4f} sn (sonuç: {sonuc1})")
    print(f"Önbellekli  adim={adim}: {sure2:.6f} sn (sonuç: {sonuc2})")
    print(f"Hızlanma: yaklaşık {sure1 / sure2:,.0f} kat")
    print(onbellekli.cache_info())  # type: ignore[attr-defined]

    # Hafta 5 Görev 1: aynı ölçüm sure_olc dekoratörüyle. Dekoratörü iç
    # fonksiyona değil dıştaki çağrıya uyguluyoruz; yoksa her özyinelemeli
    # çağrı için ayrı bir satır yazdırılırdı.
    print("sure_olc ile:")
    sure_olc(rota_sayaci_onbelleksiz(baglantilar))("dünya", adim)


if __name__ == "__main__":
    print("== Hafta 4 Görev 4: rota sayacı ==")
    rota_olcumleri()
