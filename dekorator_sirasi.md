# Dekoratör sırası: fib(20) çağrı sayıları

Ölçüm: `uv run python ornekler.py` (testi: `tests/test_dekoratorler.py::test_fib_dekorator_sirasi`)

| Tanım | fib(20) için `cagri` |
| --- | --- |
| Yalnızca `@say` | 21891 |
| `@say` üstte, `@lru_cache` altta | 39 |
| `@lru_cache` üstte, `@say` altta | 21 |

## Temel kural

Dekoratörler aşağıdan yukarıya uygulanır:

```python
@A
@B
def fib(n): ...
# fib = A(B(fib))
```

Fonksiyonun gövdesindeki `fib(n - 1)` çağrısı da `fib` adına bağlı olan **en dıştaki** katmana gider.
Yani özyinelemeli iç çağrılar da her seferinde dıştaki dekoratörden girer.

## 1) Yalnızca `@say` → 21891

Önbellek yok. `fib(n)` hem `fib(n-1)` hem `fib(n-2)` için gövdeyi baştan çalıştırır, aynı değerler
defalarca hesaplanır. Her çağrı sayaçtan geçer. fib(n) için toplam çağrı sayısı `2·F(n+1) − 1` olur:
`2 · 10946 − 1 = 21891`.

## 2) `@say` üstte, `@lru_cache` altta → 39

`fib = say(lru_cache(fib))`. Her çağrı **önce sayaca**, sonra önbelleğe gelir. Bu yüzden sayaç
önbellekte bulunan (hit) çağrıları da sayar. Ama gövde her n için yalnızca bir kez çalışır.
Gövdesi gerçekten çalışıp iki çağrı yapan değerler n = 2…20, yani 19 tane:
`19 · 2 = 38` iç çağrı + `1` dıştaki `fib(20)` çağrısı = **39**.

## 3) `@lru_cache` üstte, `@say` altta → 21

`fib = lru_cache(say(fib))`. Her çağrı **önce önbelleğe** gelir. Sayaca yalnızca önbellekte olmayan
(miss) değerler ulaşır. 0'dan 20'ye kadar her n bir kez hesaplanır: **21**.

Sayaç artık içteki katmanın niteliği olduğu için `fib.cagri` yoktur. `lru_cache` sardığı fonksiyonu
`__wrapped__` niteliğinde sakladığı için sayaca `fib.__wrapped__.cagri` ile ulaşılır.

## Sonuç

Aynı iki dekoratör farklı sırada farklı şeyleri ölçer. `@say` dışta olursa "fonksiyon kaç kez
çağrıldı?" sorusunu yanıtlar (önbellek isabetleri dahil). İçte olursa "gövde kaç kez gerçekten
çalıştı?" sorusunu yanıtlar.
