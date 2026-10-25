"""Hafta 5 için dekoratörler."""

from functools import wraps
from time import perf_counter
from typing import Callable, TypeVar, ParamSpec

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
