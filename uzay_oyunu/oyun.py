"""Basit uzay oyunu döngüsü."""

from .akis import yakit_gostergesi
from .galaksi import galaksi_kur


def hedef_menusu(hedefler: list[str]) -> str:
    """Gidilebilecek gezegenleri numaralı bir menü metni olarak döndürür."""
    satirlar = ["Nereye gitmek istersin?"]
    satirlar.extend(f"[{i}] {hedef}" for i, hedef in enumerate(hedefler, start=1))
    return "\n".join(satirlar)


def yolculuk(hedef: str, hiz: int = 1) -> str:
    """Yolculuğu özetleyen kısa metni döndürür."""
    return f"{hedef} hiz={hiz}"


def hedef_sec(secim: str, hedefler: list[str]) -> str | None:
    """Numara ya da gezegen adı olarak verilen seçimi hedefe çevirir; geçersizse None."""
    if secim.isdigit():
        sira = int(secim) - 1
        return hedefler[sira] if 0 <= sira < len(hedefler) else None
    return secim if secim in hedefler else None


def travel() -> None:
    """Gezegen hedeflerini kabul eden oyun döngüsünü çalıştırır."""
    durum = galaksi_kur()
    gosterge = yakit_gostergesi(durum["yakit"], 5)

    while True:
        hedefler = durum["baglantilar"].get(durum["konum"], [])
        print(hedef_menusu(hedefler))
        secim = input("> ").strip().lower()

        hedef = hedef_sec(secim, hedefler)
        if hedef is None:
            print("Geçersiz seçim. Bir gezegen gir.")
            continue

        try:
            durum["yakit"] = next(gosterge)
        except StopIteration:
            print("Yakıtın bitti, uzayda sürükleniyorsun…")
            break

        durum["konum"] = hedef
        print(f"{hedef} gezegenine ulaştın. Kalan yakıt: {durum['yakit']}")
