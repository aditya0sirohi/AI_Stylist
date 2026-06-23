"""
compatibility.py
Parse outfits.csv to build a compatibility map.
Each hero product_id maps to one or more outfits it appears in.
An "outfit" here = list of companion product ids + stylist rationale + metadata.
"""


# Build a dict: { hero_id: [ {companion_ids: [...], rationale: str, ...}, ... ] }
# We treat the 'hero' product as the seed, and second/layer/footwear/accessory_*
# as its companions for that outfit.
def build_compatibility_map(outfits_df):
    compat = {}

    companion_cols = ["second_id", "layer_id", "footwear_id",
                      "accessory_1_id", "accessory_2_id"]

    for _, row in outfits_df.iterrows():
        hero_id = row.get("hero_id", "")
        if not hero_id:
            continue

        companion_ids = []
        for col in companion_cols:
            cid = row.get(col, "")
            if cid and isinstance(cid, str) and cid.strip():
                companion_ids.append(cid.strip())

        outfit_entry = {
            "outfit_id": row.get("outfit_id", ""),
            "theme": row.get("theme", ""),
            "occasion": row.get("occasion", ""),
            "gender": row.get("gender", ""),
            "rationale": row.get("stylist_rationale", ""),
            "companion_ids": companion_ids,
            "total_price_inr": row.get("total_price_inr", 0),
        }

        compat.setdefault(hero_id, []).append(outfit_entry)

    return compat


# Given a hero product id, return the best outfit entry from the map.
# If no exact match, return None — caller will handle the fallback.
def get_outfit_for_hero(compat_map, hero_id, occasion_hint=None, gender_hint=None):
    if hero_id not in compat_map:
        return None

    candidates = compat_map[hero_id]

    # Prefer outfits matching the occasion and gender hints when available.
    if occasion_hint:
        filtered = [c for c in candidates if c["occasion"] == occasion_hint]
        if filtered:
            candidates = filtered
    if gender_hint:
        filtered = [c for c in candidates if c["gender"] == gender_hint]
        if filtered:
            candidates = filtered

    # Just return the first one — they're already curated by stylists.
    return candidates[0]
