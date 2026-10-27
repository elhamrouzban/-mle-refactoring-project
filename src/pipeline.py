from src.feature_engineering import (
    create_center_distance,
    create_sqft_price,
    create_water_distance
)


from src.cleaning import (
    remove_outlier,
    clean_basement,
    fill_missing_values,
)
from src.feature_engineering import create_last_known_change


def preprocessing_pipeline(df):
    df = remove_outlier(df)
    df = clean_basement(df)
    df = fill_missing_values(df)
    df = create_last_known_change(df)

    df = create_sqft_price(df)
    df = create_center_distance(df)
    df = create_water_distance(df)

    return df