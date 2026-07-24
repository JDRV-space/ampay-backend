"""Party identity rules used by current AMPAY pipeline scripts."""

TARGET_PARTY_SLUGS = [
    "fuerza_popular",
    "peru_libre",
    "renovacion_popular",
    "avanza_pais",
    "alianza_progreso",
    "somos_peru",
    "podemos_peru",
    "juntos_peru",
    "partido_morado",
]

PARTY_NAME_TO_SLUG = {
    "Fuerza Popular": "fuerza_popular",
    "Peru Libre": "peru_libre",
    "Renovacion Popular": "renovacion_popular",
    "Avanza Pais": "avanza_pais",
    "APAIS": "avanza_pais",
    "AP-PIS": "avanza_pais",
    "Alianza para el Progreso": "alianza_progreso",
    "Somos Peru": "somos_peru",
    "Podemos Peru": "podemos_peru",
    "Juntos por el Peru": "juntos_peru",
    "Partido Morado": "partido_morado",
    "SP-PM": "partido_morado",
}

PARTY_SLUG_TO_NAME = {
    "fuerza_popular": "Fuerza Popular",
    "peru_libre": "Peru Libre",
    "renovacion_popular": "Renovacion Popular",
    "avanza_pais": "Avanza Pais",
    "alianza_progreso": "Alianza para el Progreso",
    "somos_peru": "Somos Peru",
    "podemos_peru": "Podemos Peru",
    "juntos_peru": "Juntos por el Peru",
    "partido_morado": "Partido Morado",
}


def normalize_party_name(name: str) -> str | None:
    """Return a tracked party slug for a display name or alias."""
    slug = PARTY_NAME_TO_SLUG.get(name)
    if slug in TARGET_PARTY_SLUGS:
        return slug
    return None
