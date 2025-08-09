"""Value and Edge percentage calculations."""


def value_percent(ai_conf_percent: float, odds: float) -> float:
    """Return Value % = ((AI%/100) * odds - 1) * 100."""
    p = float(ai_conf_percent) / 100.0
    o = float(odds)
    return ((p * o) - 1.0) * 100.0


def edge_percent(ai_conf_percent: float, odds: float) -> float:
    """Return Edge % = (AI%/100 - 1/odds) * 100."""
    p = float(ai_conf_percent) / 100.0
    o = float(odds)
    return (p - (1.0 / o)) * 100.0
