import pandas as pd
import os
import sys
from pathlib import Path
# STEP 1: INPUT INGESTION

def read_input_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    file_path = Path(file_path)
    file_ext = file_path.suffix.lower().lstrip('.')

    if file_ext == "csv":
        df = pd.read_csv(file_path, encoding="utf-8", engine="python")
    elif file_ext in ["xlsx", "xls"]:
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        df = pd.concat(all_sheets.values(), ignore_index=True)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    return df

# STEP 2: HEADER DETECTION

def detect_header_row(df, scan_rows=10):
    best_index, best_score = 0, 0

    for i in range(min(scan_rows, len(df))):
        score = sum(
            1 for cell in df.iloc[i]
            if isinstance(cell, str) and cell.strip()
        )
        if score > best_score:
            best_score, best_index = score, i

    return best_index


def apply_header_if_needed(df, header_index):
    if header_index == 0:
        df.columns = df.columns.astype(str)
        return df.reset_index(drop=True)

    df.columns = df.iloc[header_index]
    df = df.iloc[header_index + 1:].reset_index(drop=True)
    return df


def normalize_column_names(df):
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w]+", "_", regex=True)
        .str.strip("_")
    )
    return df

# STEP 3: SEMANTIC MAPPING

STANDARD_COLUMN_SYNONYMS = {
        "created_at": [
        "created_at", "createdat",
        "date", "datetime", "date_time", "timestamp", "time",
        "review_date", "review_time",
        "posted_on", "postedon",
        "submitted_on", "submittedon",
        "created_date", "createddate",
        "entry_date", "entrytime",
        "order_date", "order_time",
        "published_at", "published",
        "reviewed_at"
    ],

    "reviewer_name": [
        "reviewer_name", "reviewername",
        "user", "username", "user_name",
        "customer", "customer_name",
        "client", "client_name",
        "buyer", "buyer_name",
        "person", "person_name",
        "author", "author_name",
        "review_by", "given_by",
        "name", "full_name", "fullname"
    ],
    "review_text": [
        "review", "review_text", "reviewtext",
        "comment", "comments",
        "feedback", "remark", "remarks",
        "opinion", "response",
        "message", "msg",
        "experience", "customer_experience",
        "review_description", "description",
        "what_you_think", "thoughts",
        "suggestion", "suggestions",
        "note", "notes"
    ],
    "rating_overall": [
        "rating", "ratings",
        "rating_overall", "ratings_overall",
        "stars", "star", "star_rating",
        "score", "overall_rating",
        "points", "points_given",
        "grade", "grade_value",
        "rate", "rated",
        "customer_rating",
        "food_rating", "service_rating",
        "rating_out_of_5", "rating_5",
        "rating_out_of_10", "rating_10"
    ],
    "like_count": [
        "like", "likes", "like_count", "likecount",
        "upvote", "upvotes",
        "helpful", "helpful_votes", "helpful_count",
        "thumbs_up", "thumbsup",
        "support", "support_count",
        "people_liked", "liked_by",
        "total_likes"
    ],
    "restaurant_name": [
        "restaurant", "restaurant_name", "restaurantname",
        "restro", "restos",
        "hotel", "hotel_name",
        "dhaba",
        "outlet", "outlet_name",
        "store", "store_name",
        "shop", "shop_name",
        "cafe", "cafe_name",
        "canteen",
        "brand", "brand_name",
        "business", "business_name",
        "name"   # common human mistake
    ],

    # CITY / LOCATION
    "city": [
        "city", "cityname",
        "town",
        "location", "area", "locality",
        "place", "place_name",
        "district",
        "region",
        "state",                 # VERY common misuse
        "address_city",
        "branch_city",
        "restaurant_city",
        "store_city"
    ],
    "primary_cuisine": [
        "primary_cuisine", "primary_cuisine_type",
        "cuisine", "cuisine_type",
        "food_type", "foodtype",
        "food_category", "category",
        "dish_type",
        "veg_nonveg", "veg_non_veg",
        "meal_type",
        "kitchen_type",
        "restaurant_type",
        "food_style"
    ],
}


def semantic_column_mapping(df, synonym_map):
    mapping = {}
    for col in df.columns:
        for std, synonyms in synonym_map.items():
            if col in synonyms:
                mapping[col] = std
                break
    return df.rename(columns=mapping)

# STEP 3.5: DUPLICATE FIX

def resolve_duplicate_columns(df):
    df = df.copy()
    dupes = df.columns[df.columns.duplicated()].unique()

    for col in dupes:
        cols = [c for c in df.columns if c == col]
        df[col] = df[cols].bfill(axis=1).iloc[:, 0]
        df = df.drop(columns=cols[1:])

    return df

# STEP 4: SCHEMA ENFORCEMENT

REQUIRED_COLUMNS = [
    "created_at",
    "reviewer_name",
    "review_text",
    "rating_overall",
    "like_count",
    "restaurant_name",
    "city",
    "primary_cuisine",
]

DEFAULT_VALUES = {
    "created_at": None,
    "reviewer_name": "anonymous",
    "review_text": "",
    "rating_overall": None,
    "like_count": 0,
    "restaurant_name": "unknown",
    "city": "unknown",
    "primary_cuisine": "unknown",
}

def enforce_schema(df):
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = DEFAULT_VALUES[col]
    return df[REQUIRED_COLUMNS]

# STEP 4.5: ROW CLEANING

def clean_rows_based_on_rating(df):
    df["rating_overall"] = pd.to_numeric(df["rating_overall"], errors="coerce")
    df = df[df["rating_overall"].notna()]

    def auto_review(row):
        if isinstance(row["review_text"], str) and row["review_text"].strip():
            return row["review_text"]

        rating_map = {
            5: "very good",
            4: "good",
            3: "average",
            2: "bad",
            1: "very bad"
        }
        return rating_map.get(int(row["rating_overall"]), "average")

    df["review_text"] = df.apply(auto_review, axis=1)
    return df

# STEP 5: TIME FEATURES

def add_and_fix_time_features(df):
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)

    if df["created_at"].isna().any():
        fallback = df["created_at"].dropna().min()
        if pd.isna(fallback):
            fallback = pd.Timestamp("1970-01-01", tz="UTC")
        df["created_at"] = df["created_at"].fillna(fallback)

    df["date"] = df["created_at"].dt.date
    df["year_month"] = (
        df["created_at"]
        .dt.tz_convert(None)
        .dt.to_period("M")
        .astype(str)
    )
    df["day_of_week"] = df["created_at"].dt.weekday
    df["hour_of_day"] = df["created_at"].dt.hour

    return df

# STEP 6: AGGREGATION

def add_restaurant_aggregates(df):
    agg = (
        df.groupby("restaurant_name")
        .agg(
            restaurant_review_count=("rating_overall", "count"),
            restaurant_overall_rating=("rating_overall", "mean")
        )
        .reset_index()
    )

    agg["restaurant_overall_rating"] = agg["restaurant_overall_rating"].round(2)
    return df.merge(agg, on="restaurant_name", how="left")


# STEP 7: EXPORT FIX

def prepare_for_export(df):
    df = df.copy()
    df["created_at"] = df["created_at"].dt.tz_convert(None)
    return df

# CORE PIPELINE FUNCTION

def standardize_restaurant_reviews(input_file_path, output_file_path=None):
    raw_df = read_input_file(input_file_path)

    df = apply_header_if_needed(raw_df, detect_header_row(raw_df))
    df = normalize_column_names(df)

    df = semantic_column_mapping(df, STANDARD_COLUMN_SYNONYMS)
    df = resolve_duplicate_columns(df)

    df = enforce_schema(df)
    df = clean_rows_based_on_rating(df)

    df = add_and_fix_time_features(df)
    df = add_restaurant_aggregates(df)

    df = prepare_for_export(df)

    if output_file_path:
        df.to_csv(output_file_path, index=False)

    return df

# CLI ENTRY POINT


# DEFAULT_INPUT = "restaurant_reviews_50k.csv"
# DEFAULT_OUTPUT = "standardized_test.csv"

# input_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
# output_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT

# df = standardize_restaurant_reviews(
#     input_file_path=input_file,
#     output_file_path=output_file
# )

# print("✅ Pipeline completed successfully")
# print(f"📤 Output file: {output_file}")
# print("📐 Total reviews:", len(df))
