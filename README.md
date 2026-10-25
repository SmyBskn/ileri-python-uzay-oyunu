# İleri Python Programlama – Uzay Oyunu (Hafta 4 ve Hafta 5 Lab)

Öğrenci: ____________________ · Numara: ____________ · GitHub: ____________________

## Kurulum ve çalıştırma

Python 3.11+ ve [uv](https://docs.astral.sh/uv/) gerekir. Proje klasöründe:

```bash
uv sync                      # .venv oluşturur, pytest'i kurar
uv run pytest                # tüm testler
uv run python main.py        # oyunu başlatır
uv run python ornekler.py    # rota ölçümü + fib(20) çağrı sayıları
uv run python istatistik.py  # map/filter/reduce sonuçları
uv run python tiktak.py      # bonus: 10 sn tik/tak
```

Oyunda gezegeni numarasıyla ya da adıyla seç; `yardim`, `envanter`, `harita` komut olarak çalışır ve
aynı menü tekrar gösterilir. Yakıt 100'dür, her yolculuk 5 harcar; 20 yolculuktan sonra yakıt biter.
Çıkmak için Ctrl+C.

## Görevlerin yeri

| Hafta / Görev | Kod | Test |
| --- | --- | --- |
| H4-1 Fibonacci üreteci | `uzay_oyunu/akis.py` → `fibonacci` | `tests/test_akis.py` |
| H4-2 Yakıt göstergesi | `akis.py` → `yakit_gostergesi`, `oyun.py` → `travel` | `test_akis.py` |
| H4-3 Seyir defteri boru hattı | `akis.py` → `satirlari_oku`, `ayristir`, `uzun_yolculuklar`; `veri/seyir.txt` | `test_akis.py` |
| H4-4 Önbellekli rota sayacı | `akis.py` → `rota_sayaci`; ölçüm `ornekler.py` | `test_akis.py` |
| H4-5 map/filter/reduce, partial | `istatistik.py` | `tests/test_istatistik.py` |
| H4 Bonus zamanlayıcı | `akis.py` → `zamanlayici`, `tiktak.py` | `test_akis.py` |
| H5-1 `sure_olc` | `uzay_oyunu/dekoratorler.py` | `tests/test_dekoratorler.py` |
| H5-2 `say` ve dekoratör sırası | `dekoratorler.py`, `ornekler.py`, `dekorator_sirasi.md` | `test_dekoratorler.py` |
| H5-3 `log_cagri` | `dekoratorler.py`; `galaksi_kur`, `hedef_menusu` üzerinde | `test_dekoratorler.py` |
| H5-4 Komut sistemi | `uzay_oyunu/komutlar.py`, `oyun.py` → `travel` | `tests/test_komutlar.py` |
| H5-5 `sinirla(alt, ust)` | `dekoratorler.py`; `oyun.py` → `yakit_harca` | `test_dekoratorler.py` |
| H5 Bonus `hafiza(maxsize)` | `dekoratorler.py` | `test_dekoratorler.py` |

## Hafta 4 Görev 4 – Rota sayacı ölçümü

Galaksi ders yönergesindeki Mars'sız galaksidir:
`say("dünya", 3), say("dünya", 10), say("dünya", 40)` → `(9, 2185, 16832258606399)`.

`rota_sayisi("dünya", 20)` (sonuç: 4315343), `time.perf_counter()` ile, Python 3.14, Windows 11:

| Sürüm | Süre |
| --- | --- |
| Önbelleksiz | 6.4672 sn |
| Önbellekli (`@lru_cache`) | 0.000972 sn |

Önbellekli sürüm yaklaşık 6 600 kat hızlı. `cache_info()` çıktısı:

```
CacheInfo(hits=47, misses=51, maxsize=None, currsize=51)
```

Önbelleksiz sürüm aynı `(gezegen, adim)` alt problemini milyonlarca kez yeniden hesaplar. Önbellekli
sürümde yalnızca 51 farklı `(gezegen, adim)` çifti hesaplanır (misses); geri kalan 47 çağrı önbellekten
gelir (hits). `@lru_cache` iç fonksiyona uygulanır; böylece özyinelemeli çağrılar da önbellekten geçer
ve her `rota_sayaci(...)` çağrısının (her galaksinin) kendi önbelleği olur.

> Süreler bilgisayara göre değişir; `uv run python ornekler.py` ile kendi makinende yeniden ölçebilirsin.

## Hafta 4 Görev 5 – Çıktılar

```
['DÜNYA', 'CENTAURI', 'SIRIUS', 'ORION', 'KARA_DELIK']
['dünya', 'centauri', 'sirius', 'orion']
10
```

## Hafta 4 Bonus – Meşgul bekleme

`zamanlayici(aralik)` döngüsü hiç durmadan saati okur ve her turda `True`/`False` üretir; `tiktak.py`
iki zamanlayıcıyı `zip` ile birlikte çeker. Bekleme sırasında işlemci boş kalmaz, bir çekirdek %100
çalışır: bu bir **meşgul beklemedir**. `time.sleep()` ise iş parçacığını uyutur: işletim sistemi süre
dolunca programı uyandırır ve arada işlemci başka işlere ayrılır.

## Hafta 5 Görev 2 – Dekoratör sırası

Ayrıntılı açıklama `dekorator_sirasi.md` dosyasında. `fib(20)` için: yalnızca `@say` → 21891;
`@say` üstte → 39; `@lru_cache` üstte → 21.
