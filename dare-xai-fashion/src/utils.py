import os
import pandas as pd


def load_products(csv_path):
    """Load products CSV file."""
    df = pd.read_csv(csv_path)
    text_cols = ["name", "brand", "category_label", "occasion",
                 "wear_type", "gender", "tags", "description"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")
    return df


def load_outfits(csv_path):
    """Load outfits CSV file."""
    df = pd.read_csv(csv_path)
    df = df.fillna("")
    return df


def build_product_text(row):
    """Combine product fields into one text string for embedding."""
    return (
        f"{row['name']} {row['category_label']} {row['occasion']} "
        f"{row['wear_type']} {row['gender']} {row['tags']} {row['description']}"
    )


def product_to_card(row, data_dir):
    """Convert product row to card dict for UI display."""
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
