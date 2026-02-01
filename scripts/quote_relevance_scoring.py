import json
import pandas as pd
import math
from collections import Counter

def generate_top_relevant_unique_quotes(
    themes_csv: str,
    multitier_json: str,
    output_csv: str,
    vague_phrases: set = None
):
    """
    Generates top relevant unique complaint quotes based on
    multi-tier importance + severity scoring.

    Selection rule:
    - If unique signals > 200 → top 5%
    - Else → top 10 signals (or all if <10)
    """

    if vague_phrases is None:
        vague_phrases = {
            "bad", "very bad", "not good", "poor",
            "quality bad", "taste bad", "food bad"
        }

    # =====================================================
    # LOAD DATA
    # =====================================================
    df = pd.read_csv(themes_csv)

    with open(multitier_json, "r", encoding="utf-8") as f:
        analysis = json.load(f)

    # Normalize text
    for col in ["phrase", "subtheme", "theme"]:
        df[col] = df[col].astype(str).str.lower().str.strip()

    # =====================================================
    # STEP 1: GLOBAL IMPORTANCE WEIGHTS
    # =====================================================

    # Tier-1: theme importance
    tier1_weights = {
        x["domain"].lower(): x["percentage"] / 100
        for x in analysis["tier_1"]["issue_distribution"]
    }

    # Tier-2: subtheme importance
    tier2_weights = {
        x["concept"].lower(): x["review_count"]
        for x in analysis["tier_2"]["quality_dimension_distribution"]
    }

    tier2_max = max(tier2_weights.values())
    tier2_weights = {k: v / tier2_max for k, v in tier2_weights.items()}

    # Tier-3: phrase importance
    phrase_weight = Counter()
    for rc in analysis["tier_3"]["top_root_causes"]:
        phrase_weight[rc["phrase"].lower()] += rc["count"]

    phrase_weight = {k: math.log1p(v) for k, v in phrase_weight.items()}

    # =====================================================
    # STEP 2: SCORE COMPONENTS
    # =====================================================

    df["severity"] = df["rating"].apply(lambda r: max(0.5, 3 - r))
    df["theme_weight"] = df["theme"].map(tier1_weights).fillna(0.1)
    df["subtheme_weight"] = df["subtheme"].map(tier2_weights).fillna(0.05)
    df["phrase_weight"] = df["phrase"].map(phrase_weight).fillna(0.3)

    df["specificity"] = df["phrase"].apply(
        lambda p: 0.3 if p in vague_phrases else 1.0
    )

    # =====================================================
    # STEP 3: FINAL RELEVANCE SCORE
    # =====================================================
    df["relevance_score"] = (
        df["severity"]
        * df["theme_weight"]
        * df["subtheme_weight"]
        * df["phrase_weight"]
        * df["specificity"]
    )

    # =====================================================
    # STEP 4: CREATE SIGNAL KEY
    # =====================================================
    df["signal_key"] = list(
        zip(df["theme"], df["subtheme"], df["phrase"])
    )

    # =====================================================
    # STEP 5: ONE REPRESENTATIVE QUOTE PER SIGNAL
    # =====================================================
    df_rep = (
        df.sort_values(
            ["relevance_score", "rating", "phrase"],
            ascending=[False, True, False]
        )
        .groupby("signal_key", as_index=False)
        .first()
    )

    # =====================================================
    # STEP 6: RANK & SELECT SIGNALS
    # =====================================================
    df_rep = df_rep.sort_values("relevance_score", ascending=False)

    total_signals = len(df_rep)

    df_top = (
        df_rep.sort_values("relevance_score", ascending=False).head(5)
    )

    # =====================================================
    # STEP 7: OUTPUT
    # =====================================================
    output_columns = [
        "review_id",
        "theme",
        "subtheme",
        "phrase",
        "rating",
        "relevance_score"
    ]

    df_top[output_columns].to_csv(output_csv, index=False)

    print("✅ Quote relevance scoring complete")
    print(f"📄 Output file: {output_csv}")
    print(f"🔢 Unique signals ranked: {total_signals}")
    print(f"⭐ Top signals returned: {len(df_top)}")

    return df_top[output_columns].to_dict(orient="records")

# generate_top_relevant_unique_quotes(
#     themes_csv="themes_test.csv",
#     multitier_json="multitier_analysis_output.json",
#     output_csv="top_relevant_unique_quotes.csv"
# )
