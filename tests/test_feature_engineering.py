import pandas as pd


from src.feature_engineering import (
    create_last_known_change,
    create_sqft_price,
    create_center_distance,
    create_water_distance
    )


def test_create_last_known_change():
    df = pd.DataFrame({
        "yr_built": [1990, 2000],
        "yr_renovated": [0, 2015]
    })

    result = create_last_known_change(df)

    assert result["last_known_change"].tolist() == [1990, 2015]
    assert "yr_built" not in result.columns
    assert "yr_renovated" not in result.columns

def test_create_sqft_price():
    df = pd.DataFrame({
        "price": [300000, 450000],
        "sqft_living": [1000, 2000],
        "sqft_lot": [2000, 3000]
    })

    result = create_sqft_price(df)

    assert result["sqft_price"].tolist() == [100.0, 90.0]


def test_create_center_distance():
    df = pd.DataFrame({
        "lat": [47.62774],
        "long": [-122.24194]
    })

    result = create_center_distance(df)

    assert result["center_distance"].iloc[0] == 0


def test_create_water_distance():
    df = pd.DataFrame({
        "waterfront": [1, 0],
        "lat": [47.6, 47.6],
        "long": [-122.3, -122.3]
    })

    result = create_water_distance(df)

    assert result["water_distance"].tolist() == [0, 0]