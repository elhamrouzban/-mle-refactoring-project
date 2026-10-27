from src.pipeline import preprocessing_pipeline
import pandas as pd
from src.modeling import train_model


kc_data = pd.read_csv("data/King_County_House_prices_dataset.csv")

df = kc_data.copy()
cleaned_df = preprocessing_pipeline(df)

train_model(cleaned_df)


print("Original:", kc_data.shape)
print("Cleaned:", cleaned_df.shape)
print("Missing values:", cleaned_df.isna().sum().sum())
print("Columns:", cleaned_df.columns.tolist())