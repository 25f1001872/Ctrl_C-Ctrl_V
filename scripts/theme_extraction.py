import re
import json
import pandas as pd

# =========================
# STOPWORDS (SAFE LIST)
# =========================
STOPWORDS = {
    "was", "is", "are", "were",
    "the", "a", "an",
    "and", "or", "but",
    "this", "that", "there",
    "then", "very", "really"
}

# =========================
# TEXT NORMALIZATION
# =========================
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# =========================
# THEME EXTRACTION (CORE ENGINE)
# =========================
def extract_themes(review_text: str, phrase_keywords, token_keywords):
    clean_text = normalize_text(review_text)
    tokens = clean_text.split()
    filtered_tokens = [t for t in tokens if t not in STOPWORDS]

    hits = []

    # 1️⃣ Phrase matching (highest precision)
    for item in phrase_keywords:
        if item["phrase"] in clean_text:
            hits.append(item)

    # 2️⃣ Token matching (fallback)
    token_set = set(filtered_tokens)
    for item in token_keywords:
        if item["phrase"] in token_set:
            hits.append(item)

    # 3️⃣ Deduplicate matches
    unique_hits = {
        (h["theme"], h["subtheme"], h["polarity"], h["phrase"]): h
        for h in hits
    }

    return list(unique_hits.values())

# =========================
# STRUCTURED OUTPUT BUILDER
# =========================
def build_theme_structure(matches):
    output = {}

    for m in matches:
        theme = m["theme"]
        subtheme = m["subtheme"] or "general"
        polarity = m["polarity"]

        output.setdefault(theme, {})
        output[theme].setdefault(subtheme, {})
        output[theme][subtheme].setdefault(polarity, [])

        output[theme][subtheme][polarity].append(m["phrase"])

    return output

def flatten_extracted_themes(theme_dict, review_index, rating):
    rows = []
    for theme, subthemes in theme_dict.items():
        for subtheme, polarities in subthemes.items():
            for polarity, phrases in polarities.items():
                for phrase in phrases:
                    rows.append({
                        "review_id": review_index,
                        "rating": rating,
                        "theme": theme,
                        "subtheme": subtheme,
                        "polarity": polarity,
                        "phrase": phrase
                    })
    return rows
def analyze_recurring_theme_concerns_json(
    themes_df: pd.DataFrame,
    min_review_coverage: int = 3,
    negative_ratio_threshold: float = 0.6,
    max_avg_rating: float = 3.0,
    top_k: int = 10
):
    agg = (
        themes_df
        .groupby(["theme", "subtheme"])
        .agg(
            total_mentions=("phrase", "count"),
            unique_reviews=("review_id", "nunique"),
            negative_mentions=("polarity", lambda x: (x == "negative").sum()),
            avg_rating=("rating", "mean")
        )
        .reset_index()
    )

    agg["negative_ratio"] = agg["negative_mentions"] / agg["total_mentions"]
    agg["concern_score"] = (
        agg["unique_reviews"]
        * agg["negative_ratio"]
        * (3.5 - agg["avg_rating"])
    )

    genuine = agg[
        (agg["unique_reviews"] >= min_review_coverage) &
        (agg["negative_ratio"] >= negative_ratio_threshold) &
        (agg["avg_rating"] <= max_avg_rating)
    ].sort_values("concern_score", ascending=False).head(top_k)

    return genuine.to_dict(orient="records")


# =========================
# 🚀 MAIN REUSABLE FUNCTION
# =========================
def run_theme_extraction(
    input_csv: str,
    flattened_keywords_json: str,
    output_csv: str,
    review_text_column: str = "review_text",
    rating_column: str = "rating_overall"
):
    with open(flattened_keywords_json, "r", encoding="utf-8") as f:
        flat_keywords = json.load(f)

    phrase_keywords = [k for k in flat_keywords if " " in k["phrase"]]
    token_keywords  = [k for k in flat_keywords if " " not in k["phrase"]]

    df = pd.read_csv(input_csv)
    reviews = df[review_text_column]
    ratings = df[rating_column]

    all_rows = []

    for idx, (review, rating) in enumerate(zip(reviews, ratings)):
        matches = extract_themes(review, phrase_keywords, token_keywords)
        themes = build_theme_structure(matches)
        flat_rows = flatten_extracted_themes(themes, idx, rating)
        all_rows.extend(flat_rows)

    themes_df = pd.DataFrame(all_rows)
    themes_df.to_csv(output_csv, index=False)

    # 🔍 JSON insight generation
    concerns_json = analyze_recurring_theme_concerns_json(themes_df)

    result = {
        "summary": {
            "total_reviews_processed": len(df),
            "total_theme_mentions": len(themes_df),
        },
        "top_genuine_concerns": concerns_json,
        # "raw_theme_rows": themes_df.to_dict(orient="records")
    }
    
    return result



# from theme_extractor import run_theme_extraction

# run_theme_extraction(
#     input_csv="standardized_test.csv",
#     flattened_keywords_json="flattened_keywords.json",
#     output_csv="themes_test.csv"
# )