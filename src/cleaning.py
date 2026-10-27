
def remove_outlier(df):
    outliers = df.query("bedrooms == 33")
    return df.drop(outliers.index)


def clean_basement(df):
    df["sqft_basement"] = df["sqft_living"] - df["sqft_above"]
    return df


def fill_missing_values(df):
    df["waterfront"] = df["waterfront"].fillna(0)
    df["view"] = df["view"].fillna(0)
    return df