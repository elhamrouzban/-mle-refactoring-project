
import pandas as pd

from src.pipeline import preprocessing_pipeline


def test_preprocessing_pipeline():
    df = pd.DataFrame({
        "bedrooms": [3, 4],
        "sqft_living": [2000, 2500],
        "sqft_above": [1600, 2000],
        "sqft_lot": [4000, 5000],
        "waterfront": [1, 0],
        "view": [None, 2],
        "yr_built": [1990, 2000],
        "yr_renovated": [0, 2015],
        "price": [300000, 450000],
        "lat": [47.6, 47.6],
        "long": [-122.3, -122.3],
    })

    result = preprocessing_pipeline(df)

    assert len(result) == 2
    assert result["sqft_basement"].tolist() == [400, 500]
    assert result["last_known_change"].tolist() == [1990, 2015]
    assert result["sqft_price"].tolist() == [50.0, 60.0]
    assert result["view"].tolist() == [0, 2]
    assert result["water_distance"].tolist() == [0, 0]
