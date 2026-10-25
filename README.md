# İleri Python Programlama – Uzay Oyunu

Öğrenci: ____________________ · Numara: ____________ · GitHub: ____________________

## Kurulum ve çalıştırma

Python 3.11+ ve [uv](https://docs.astral.sh/uv/) gerekir. Proje klasöründe:

```bash
uv sync                      # .venv oluşturur, pytest'i kurar
uv run pytest                # tüm testler
uv run python main.py        # oyunu başlatır
uv run python ornekler.py    # rota ölçümü
```

Gezegeni numarasıyla ya da adıyla seç. Çıkmak için Ctrl+C.

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
