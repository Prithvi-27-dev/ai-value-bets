import math
from value_calc import value_percent, edge_percent

def approx(a, b, eps=1e-6):
    return abs(a - b) <= eps

def test_liverpool_example():
    # 72% at 2.10 -> 51.2% value, ~24.381% edge
    assert approx(value_percent(72, 2.10), 51.2, 1e-6)
    assert approx(edge_percent(72, 2.10), 24.381, 1e-3)

def test_psg_over_example():
    # 81% at 1.90 -> 53.9% value, ~28.368% edge
    assert approx(value_percent(81, 1.90), 53.9, 1e-6)
    assert approx(edge_percent(81, 1.90), 28.368, 1e-3)

def test_rm_btts_example():
    # 65% at 1.95 -> 26.75% value, ~13.718% edge
    assert approx(value_percent(65, 1.95), 26.75, 1e-6)
    assert approx(edge_percent(65, 1.95), 13.718, 1e-3)

def test_bounds_and_types():
    # Strings should coerce
    assert approx(value_percent("72", "2.10"), 51.2, 1e-6)
    assert approx(edge_percent("72", "2.10"), 24.381, 1e-3)

# --- Extra coverage for BTTS and Over/Under ---

def test_btts_yes():
    # Example: BTTS Yes 58% at 1.85
    # value = (0.58*1.85 - 1)*100 = (1.073 - 1)*100 = 7.3%
    # edge  = (0.58 - 1/1.85)*100 = (0.58 - 0.5405405)*100 ≈ 3.946%
    assert approx(value_percent(58, 1.85), 7.3, 1e-6)
    assert approx(edge_percent(58, 1.85), 3.946, 1e-3)

def test_over25():
    # Example: Over 2.5 Goals 62% at 1.80
    # value = (0.62*1.80 - 1)*100 = (1.116 - 1)*100 = 11.6%
    # edge  = (0.62 - 1/1.80)*100 = (0.62 - 0.5555556)*100 ≈ 6.444%
    assert approx(value_percent(62, 1.80), 11.6, 1e-6)
    assert approx(edge_percent(62, 1.80), 6.444, 1e-3)
