"""Hafta 4 bonus: 10 saniye boyunca her 2 sn'de "tik", her 5 sn'de "tak" yazar.

Neden meşgul bekleme? zamanlayici() içindeki döngü hiç durmadan saati okur;
zip her turda iki üreteçten de bir değer çeker. Bekleme sırasında işlemci boş
durmaz, bir çekirdeği %100 meşgul eder (Görev Yöneticisi'nde görülebilir).

time.sleep(aralik) ise iş parçacığını işletim sistemine bırakır: süre dolana
kadar program hiç çalışmaz ve işlemci başka işlere ayrılır. Bu yüzden basit
bekleme için time.sleep tercih edilir; meşgul bekleme yalnızca çok kısa ve
hassas zamanlama gerektiğinde mantıklıdır.
"""

from time import perf_counter

from uzay_oyunu.akis import zamanlayici


def tik_tak(sure: float = 10) -> None:
    """`sure` saniye boyunca iki zamanlayıcıyı birlikte çalıştırır."""
    baslangic = perf_counter()
    for tik, tak in zip(zamanlayici(2), zamanlayici(5)):
        gecen = perf_counter() - baslangic
        if gecen > sure + 0.1:
            break
        if tik:
            print(f"{gecen:4.1f} sn: tik")
        if tak:
            print(f"{gecen:4.1f} sn: tak")


if __name__ == "__main__":
    tik_tak()
