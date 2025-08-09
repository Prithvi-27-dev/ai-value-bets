def value_percent(ai_conf_percent: float, odds: float) -> float:
    p = float(ai_conf_percent) / 100.0
    o = float(odds)
    return ((p * o) - 1.0) * 100.0

def edge_percent(ai_conf_percent: float, odds: float) -> float:
    p = float(ai_conf_percent) / 100.0
    o = float(odds)
    return (p - (1.0 / o)) * 100.0