"""Hafta 4 yönergesindeki üreteçler ve rota hesabı."""

from typing import Iterable, Iterator


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
