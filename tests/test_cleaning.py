import pandas as pd 
import numpy as np
from src.cleaning import (
    remove_outlier,
    clean_basement,
    fill_missing_values
    )


def test_remove_outlier():
    df = pd.DataFrame({"bedrooms": [1, 2, 33, 4]})
    result = remove_outlier(df)

    assert result["bedrooms"].tolist() == [1, 2, 4]



def test_clean_basement():
    df = pd.DataFrame({
        "sqft_living": [2000, 1500],
        "sqft_above": [1600, 1500]
    })

    result = clean_basement(df)

    assert result["sqft_basement"].tolist() == [400, 0]

def test_fill_missing_values():
    df = pd.DataFrame({
        "waterfront": [1, np.nan],
        "view": [np.nan, 2]
    })

    result = fill_missing_values(df)

    assert result["waterfront"].tolist() == [1, 0]
    assert result["view"].tolist() == [0, 2]