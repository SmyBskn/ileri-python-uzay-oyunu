"""Hafta 5 için dekoratörler."""

from collections import OrderedDict
from functools import wraps
from time import perf_counter
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def sure_olc(func: Callable[P, R]) -> Callable[P, R]:
    """Fonksiyonun çalışma süresini ölçer ve sonucu değiştirmeden döndürür."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        baslangic = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            sure = perf_counter() - baslangic
            print(f"{func.__name__}: {sure:.4f} sn")
    return wrapper


def say(func: Callable[P, R]) -> Callable[P, R]:
    """Fonksiyonun sarmalayıcı üzerinden kaç kez çağrıldığını niteliğinde tutar."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        wrapper.cagri += 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)
    wrapper.cagri = 0  # type: ignore[attr-defined]
    return wrapper


def log_cagri(func: Callable[P, R]) -> Callable[P, R]:
    """Çağrıdan önce fonksiyon ve argümanları, sonra dönüş değerini yazdırır."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        parcalar = [repr(arg) for arg in args]
        parcalar.extend(f"{ad}={deger!r}" for ad, deger in kwargs.items())
        print(f"-> {func.__name__}({', '.join(parcalar)})")
        sonuc = func(*args, **kwargs)
        print(f"<- {func.__name__} = {sonuc!r}")
        return sonuc
    return wrapper


def sinirla(alt: int | float, ust: int | float) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """İlk argümanı belirtilen kapalı aralıkta değilse ValueError verir."""
    def dekorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if args:
                deger = args[0]
            elif func.__code__.co_varnames[0] in kwargs:
                deger = kwargs[func.__code__.co_varnames[0]]
            else:
                raise TypeError(f"{func.__name__} ilk argümanını almalıdır")
            if not alt <= deger <= ust:
                raise ValueError(
                    f"{func.__name__}: {deger} değeri {alt}-{ust} aralığında değil"
                )
            return func(*args, **kwargs)
        return wrapper
    return dekorator


def hafiza(maxsize: int | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Sözlük tabanlı önbellek; maxsize verilirse en eski girdiyi siler."""
    if maxsize is not None and maxsize < 0:
        raise ValueError("maxsize negatif olamaz")

    def dekorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: OrderedDict[tuple[Any, ...], R] = OrderedDict()

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            anahtar = (args, tuple(sorted(kwargs.items())))
            if anahtar in cache:
                cache.move_to_end(anahtar)
                return cache[anahtar]
            sonuc = func(*args, **kwargs)
            if maxsize != 0:
                cache[anahtar] = sonuc
                if maxsize is not None and len(cache) > maxsize:
                    cache.popitem(last=False)
            return sonuc

        wrapper.cache = cache  # type: ignore[attr-defined]
        return wrapper
    return dekorator
