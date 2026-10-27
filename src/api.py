from fastapi import FastAPI
import skops.io as sio
from pydantic import BaseModel
from functools import lru_cache

import pandas as pd
from fastapi import HTTPException


class HouseFeatures(BaseModel):
    id: int
    bedrooms: int
    bathrooms: float
    sqft_living: int
    sqft_lot: int
    floors: float
    waterfront: int
    view: int
    condition: int
    grade: int
    sqft_above: int
    sqft_basement: int
    zipcode: int
    lat: float
    long: float
    sqft_living15: int
    sqft_lot15: int
    last_known_change: int
    center_distance: float
    water_distance: float



app = FastAPI()


@app.get("/")
def home():
    return {"message": "House Price API is running"}


@lru_cache
def load_model():
    return sio.load(
        "model/model.bin",
        trusted=sio.get_untrusted_types(file="model/model.bin"),
    )


@app.post("/predict")
def predict(features: HouseFeatures):
    try:
        df = pd.DataFrame([features])
        prediction = load_model().predict(df)[0]
        return {"predicted_price": float(prediction)}
    except (ValueError, KeyError) as error:
        raise HTTPException(status_code=422, detail=str(error))