"""Hafta 4 yönergesindeki üreteçler ve rota hesabı."""

from functools import lru_cache
from typing import Callable, Iterable, Iterator


def fibonacci() -> Iterator[int]:
    """Sonsuz Fibonacci sayılarını sırayla üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki


def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    """Her adımda yakıt tüketip kalan yakıtı üretir; sıfırdan sonra durur."""
    if tuketim <= 0:
        raise ValueError("tuketim pozitif olmalıdır")
    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit


def rota_sayaci(baglantilar: dict[str, list[str]]) -> Callable[[str, int], int]:
    """Verilen bağlantılar için önbellekli rota sayma fonksiyonunu döndürür.

    Önbellek iç fonksiyonda durur; böylece her galaksinin kendi önbelleği olur
    ve özyinelemeli çağrılar da önbellekten geçer.
    """
    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Gezegenden başlayıp tam adim yolculuk yapan rotaları sayar."""
        if adim == 0:
            return 1
        return sum(
            rota_sayisi(komsu, adim - 1)
            for komsu in baglantilar.get(gezegen, [])
        )
    return rota_sayisi


def rota_sayaci_onbelleksiz(baglantilar: dict[str, list[str]]) -> Callable[[str, int], int]:
    """Karşılaştırma amacıyla önbelleksiz rota sayma fonksiyonunu döndürür."""
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Gezegenden başlayıp tam adim yolculuk yapan rotaları sayar."""
        if adim == 0:
            return 1
        return sum(
            rota_sayisi(komsu, adim - 1)
            for komsu in baglantilar.get(gezegen, [])
        )
    return rota_sayisi


def satirlari_oku(yol: str) -> Iterator[str]:
    """Dosyadan boş ve yorum satırları hariç satırları tembel biçimde üretir."""
    with open(yol, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                yield satir


def ayristir(satirlar: Iterable[str]) -> Iterator[tuple[str, str, int]]:
    """'kaynak -> hedef yakıt' satırlarını (kaynak, hedef, yakit) demetlerine dönüştürür."""
    for satir in satirlar:
        kaynak_hedef, yakit_metni = satir.rsplit(maxsplit=1)
        kaynak, hedef = (parca.strip() for parca in kaynak_hedef.split("->", 1))
        yield kaynak, hedef, int(yakit_metni)


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]], esik: int
) -> Iterator[tuple[str, str, int]]:
    """Yakıt tüketimi eşikten büyük olan yolculuk kayıtlarını üretir."""
    for kayit in kayitlar:
        if kayit[2] > esik:
            yield kayit
