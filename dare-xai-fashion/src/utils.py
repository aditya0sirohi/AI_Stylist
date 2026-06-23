"""
utils.py
Helper functions for loading data and small formatting tasks.
Keep this file boring and simple — just CSV loaders and tiny helpers.
"""

import os
import pandas as pd


# Loads products.csv into a pandas DataFrame and returns it.
def load_products(csv_path):
    df = pd.read_csv(csv_path)
    # fill missing text fields so embedding strings don't crash
    text_cols = ["name", "brand", "category_label", "occasion",
                 "wear_type", "gender", "tags", "description"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")
    return df


# Loads outfits.csv into a pandas DataFrame and returns it.
def load_outfits(csv_path):
    df = pd.read_csv(csv_path)
    df = df.fillna("")
    return df


# Build the combined text string we feed to the sentence-transformer model.
# Richer text = better retrieval on a small dataset.
def build_product_text(row):
    return (
        f"{row['name']} {row['category_label']} {row['occasion']} "
        f"{row['wear_type']} {row['gender']} {row['tags']} {row['description']}"
    )


# Convert a product DataFrame row into a simple dict for the UI.
def product_to_card(row, data_dir):
    image_rel = row.get("image", "")
    image_path = os.path.join(data_dir, image_rel) if image_rel else ""
    return {
        "id": row["id"],
        "name": row["name"],
        "brand": row["brand"],
        "price_inr": int(row["price_inr"]) if pd.notna(row.get("price_inr", None)) else 0,
        "rating": float(row["rating"]) if pd.notna(row.get("rating", None)) else None,
        "occasion": row["occasion"],
        "category_label": row["category_label"],
        "image_path": image_path if os.path.exists(image_path) else "",
    }
