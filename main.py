"""Uzay oyununu başlatır: uv run python main.py"""
from uzay_oyunu.oyun import travel

if __name__ == "__main__":
    try:
        travel()
    except (KeyboardInterrupt, EOFError):
        print("\nOyundan çıkıldı.")
