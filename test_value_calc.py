import pandas as pd

def calculate_value(ai_confidence, odds):
    ai_prob = ai_confidence / 100.0
    return ((ai_prob * odds) - 1.0) * 100.0

def test_value_percentages():
    # Example: 72% at odds 2.10 → ~51.2%
    assert round(calculate_value(72, 2.10), 1) == 51.2
    # Example: 81% at odds 1.90 → ~53.9%
    assert round(calculate_value(81, 1.90), 1) == 53.9
    # Example: 65% at odds 1.95 → ~26.8%
    assert round(calculate_value(65, 1.95), 1) == 26.8

if __name__ == "__main__":
    test_value_percentages()
    print("✅ All value % tests passed.")