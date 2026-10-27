import pandas as pd


from src.feature_engineering import create_last_known_change


def test_create_last_known_change():
    df = pd.DataFrame({
        "yr_built": [1990, 2000],
        "yr_renovated": [0, 2015]
    })

    result = create_last_known_change(df)

    assert result["last_known_change"].tolist() == [1990, 2015]
    assert "yr_built" not in result.columns
    assert "yr_renovated" not in result.columns