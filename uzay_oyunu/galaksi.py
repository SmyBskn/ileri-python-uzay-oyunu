"""Galaksi tanımları ve temel oyun durumu."""

from typing import Any

GALAKSI: dict[str, Any] = {
    "konum": "dünya",
    # Ders yönergesindeki (Mars'sız) galaksi: rota_sayisi("dünya", 3) == 9
    "baglantilar": {
        "dünya": ["centauri", "sirius"],
        "centauri": ["dünya", "orion"],
        "sirius": ["orion", "dünya", "kara_delik"],
        "orion": ["centauri", "sirius"],
        "kara_delik": ["sirius"],
    },
    "credits": 100,
    "engines": ["standart motor"],
    "copilot": "yok",
    "yakit": 100,
}


def galaksi_kur() -> dict[str, Any]:
    """Yeni bir oyun için başlangıç galaksisi ve durum sözlüğü döndürür."""
    return {
        "konum": GALAKSI["konum"],
        "baglantilar": {
            gezegen: list(komsular)
            for gezegen, komsular in GALAKSI["baglantilar"].items()
        },
        "credits": GALAKSI["credits"],
        "engines": list(GALAKSI["engines"]),
        "copilot": GALAKSI["copilot"],
        "yakit": GALAKSI["yakit"],
    }
