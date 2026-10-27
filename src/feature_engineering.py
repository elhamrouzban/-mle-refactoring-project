import numpy as np

def create_last_known_change(df):
    df["last_known_change"] = np.where(
        df["yr_renovated"].notna() & (df["yr_renovated"] != 0),
        df["yr_renovated"],
        df["yr_built"]
    ).astype(int)

    df.drop(columns=["yr_built", "yr_renovated"], inplace=True)
    return df


def create_sqft_price(df):
    df["sqft_price"] = (
        df["price"] / (df["sqft_living"] + df["sqft_lot"])
    ).round(2)
    return df


def create_center_distance(df):

    df["delta_lat"] = np.absolute(47.62774 - df["lat"])
    df["delta_long"] = np.absolute(-122.24194 - df["long"])
    df["center_distance"] = (
        (
            (df["delta_long"] * np.cos(np.radians(47.6219))) ** 2
            + df["delta_lat"] ** 2
        )
        ** (1 / 2)
        * 2
        * np.pi
        * 6378
        / 360
    )

    return df


def dist(long, lat, ref_long, ref_lat):
    delta_long = long - ref_long
    delta_lat = lat - ref_lat
    delta_long_corr = delta_long * np.cos(np.radians(ref_lat))

    return (
        (delta_long_corr**2 + delta_lat**2)**0.5
        * 2 * np.pi * 6378 / 360
    )


def create_water_distance(df):
    water_list = df.query("waterfront == 1")
    water_coords = list(zip(water_list["long"], water_list["lat"]))
    water_distance = []

    for lon, lat in zip(df["long"], df["lat"]):
        ref_list = []

        for x, y in water_coords:
            distance = dist(lon, lat, x, y)
            ref_list.append(distance)

        water_distance.append(min(ref_list))

    df["water_distance"] = water_distance
    return df
