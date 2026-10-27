import pandas as pd 
from src.cleaning import remove_outlier


def test_remove_outlier():
    df = pd.DataFrame({"bedrooms": [1, 2, 33, 4]})
    result = remove_outlier(df)

    assert result["bedrooms"].tolist() == [1, 2, 4]