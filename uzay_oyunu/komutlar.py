"""Oyundaki komutları kaydeden dekoratör ve komut işleyicileri."""

from typing import Any, Callable

KomutFonksiyonu = Callable[[dict[str, Any]], str]

KOMUTLAR: dict[str, tuple[KomutFonksiyonu, str]] = {}


def komut(ad: str, aciklama: str = "") -> Callable[[KomutFonksiyonu], KomutFonksiyonu]:
    """Fonksiyonu değiştirmeden ad ve açıklamayla KOMUTLAR sözlüğüne kaydeder.

    Kayıt tanım anında yapılır; aynı ad ikinci kez kullanılırsa ValueError verir.
    Sarmalayıcı yoktur, bu yüzden wraps gerekmez: aynı fonksiyon geri döner.
    """
    def dekorator(func: KomutFonksiyonu) -> KomutFonksiyonu:
        if ad in KOMUTLAR:
            raise ValueError(f"{ad!r} komutu zaten kayıtlı")
        KOMUTLAR[ad] = (func, aciklama)
        return func
    return dekorator


@komut("yardim", "komutları listeler")
def yardim(durum: dict[str, Any]) -> str:
    """Kayıtlı komut adlarını ve açıklamalarını listeler."""
    return "\n".join(
        f"{ad} {aciklama}".rstrip()
        for ad, (_, aciklama) in sorted(KOMUTLAR.items())
    )


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: dict[str, Any]) -> str:
    """Motor, yardımcı pilot ve kredi durumunu gösterir."""
    return (
        f"Motorlar: {', '.join(durum.get('engines', []))}\n"
        f"Yardımcı pilot: {durum.get('copilot', 'yok')}\n"
        f"Kredi: {durum.get('credits', 0)}"
    )


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: dict[str, Any]) -> str:
    """Mevcut konumdan ulaşılabilen gezegenleri gösterir."""
    konum = durum.get("konum", "")
    gezegenler = durum.get("baglantilar", {}).get(konum, [])
    return ", ".join(gezegenler) if gezegenler else "Gidilebilecek gezegen yok."
