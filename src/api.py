from fastapi import (
    FastAPI, 
    Depends,
)
import skops.io as sio
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import pandas as pd
from fastapi import HTTPException


from src.database import get_db
from functools import lru_cache
from src.database import Base, engine
from src.database_models import House


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

class HouseCreate(BaseModel):
    id: int = Field(gt=0)
    bedrooms: int = Field(ge=0)
    bathrooms: float = Field(ge=0)
    sqft_living: int = Field(gt=0)
    price: float = Field(gt=0)

app = FastAPI()

Base.metadata.create_all(bind=engine)

class HouseUpdate(BaseModel):
    bedrooms: int
    bathrooms: float
    sqft_living: int
    price: float



@lru_cache
def load_model():
    return sio.load(
        "model/model.bin",
        trusted=sio.get_untrusted_types(file="model/model.bin"),
    )

@app.get("/")
def home():
    return {"message": "House Price API is running"}


@app.post("/predict")
def predict(features: HouseFeatures):
    try:
        df = pd.DataFrame([features.model_dump()])

        model = load_model()
        df = df[model.feature_names_in_]

        prediction = model.predict(df)[0]

        return {"predicted_price": float(prediction)}

    except (ValueError, KeyError) as error:
        raise HTTPException(status_code=422, detail=str(error))


@app.post("/houses", status_code=201)
def create_house(
    house: HouseCreate,
    db: Session = Depends(get_db)
):
    new_house = House(**house.model_dump())
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house


@app.get("/houses")
def get_houses(db: Session = Depends(get_db)):
    houses = db.query(House).all()
    return houses


@app.get("/houses/{house_id}")
def get_house(house_id: int, db: Session = Depends(get_db)):
    house = db.get(House, house_id)

    if house is None:
        raise HTTPException(
            status_code=404,
            detail="House not found"
        )

    return house



@app.put("/houses/{house_id}")
def update_house(
    house_id: int,
    house_data: HouseUpdate,
    db: Session = Depends(get_db)
):
    house = db.get(House, house_id)

    if house is None:
        raise HTTPException(
            status_code=404,
            detail="House not found"
        )

    house.bedrooms = house_data.bedrooms
    house.bathrooms = house_data.bathrooms
    house.sqft_living = house_data.sqft_living
    house.price = house_data.price

    db.commit()

    db.refresh(house)

    return house



@app.delete("/houses/{house_id}")
def delete_house(
    house_id: int,
    db: Session = Depends(get_db)
):
    house = db.get(House, house_id)

    if house is None:
        raise HTTPException(
            status_code=404,
            detail="House not found"
        )

    db.delete(house)

    db.commit()

    return {"message": "House deleted successfully"}
