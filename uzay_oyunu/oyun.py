"""Basit uzay oyunu döngüsü."""

from .akis import yakit_gostergesi
from .dekoratorler import log_cagri, sinirla
from .galaksi import galaksi_kur
from .komutlar import KOMUTLAR


@log_cagri
def hedef_menusu(hedefler: list[str]) -> str:
    """Gidilebilecek gezegenleri numaralı bir menü metni olarak döndürür."""
    satirlar = ["Nereye gitmek istersin?"]
    satirlar.extend(f"[{i}] {hedef}" for i, hedef in enumerate(hedefler, start=1))
    return "\n".join(satirlar)


def yolculuk(hedef: str, hiz: int = 1) -> str:
    """Yolculuğu özetleyen kısa metni döndürür."""
    return f"{hedef} hiz={hiz}"


@sinirla(0, 100)
def yakit_harca(miktar: int) -> int:
    """Belirtilen miktarda yakıt harcar ve kalan yakıtı döndürür."""
    return 100 - miktar


def hedef_sec(secim: str, hedefler: list[str]) -> str | None:
    """Numara ya da gezegen adı olarak verilen seçimi hedefe çevirir; geçersizse None."""
    if secim.isdigit():
        sira = int(secim) - 1
        return hedefler[sira] if 0 <= sira < len(hedefler) else None
    return secim if secim in hedefler else None


def travel() -> None:
    """Komutları veya gezegen hedeflerini kabul eden oyun döngüsünü çalıştırır."""
    durum = galaksi_kur()
    gosterge = yakit_gostergesi(durum["yakit"], 5)

    while True:
        hedefler = durum["baglantilar"].get(durum["konum"], [])
        print(hedef_menusu(hedefler))
        secim = input("> ").strip().lower()

        # Girdi bir komut adıysa komutu çalıştır, aynı menüyü tekrar göster.
        if secim in KOMUTLAR:
            fonksiyon, _aciklama = KOMUTLAR[secim]
            print(fonksiyon(durum))
            continue

        hedef = hedef_sec(secim, hedefler)
        if hedef is None:
            print("Geçersiz seçim. Bir gezegen veya komut gir.")
            continue

        try:
            durum["yakit"] = next(gosterge)
        except StopIteration:
            print("Yakıtın bitti, uzayda sürükleniyorsun…")
            break

        durum["konum"] = hedef
        print(f"{hedef} gezegenine ulaştın. Kalan yakıt: {durum['yakit']}")
