import json
import pandas as pd
from collections import defaultdict, Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# =========================================================
# CONFIG
# =========================================================
REVIEWS_CSV = BASE_DIR / "standardized_output.csv"
THEMES_CSV = BASE_DIR / "themes_test.csv"
RULE_KEYWORDS_JSON = BASE_DIR / "rule_keywords.json"
FOOD_ONTOLOGY_JSON = BASE_DIR / "food_domain_ontology.json"
REVIEW_TEXT_COLUMN = "review_text"
# =========================================================
# TIER-2 CONFIG (must match themes_test.csv)
# =========================================================
TIER2_FOOD_SUBTHEMES = {
    "texture",
    "freshness",
    "temperature",
    "spice_level",
    "salt_sweet_balance",
    "portion_size"
}

# =========================================================
# RULE-BASED CLASSIFIER (TIER-1)
# =========================================================
def rule_based_classify(text: str, rule_map: dict):
    text = text.lower()
    domain_hits = defaultdict(int)
    matched_anchor = None

    for domain, keywords in rule_map.items():
        for kw in keywords:
            if kw in text:
                domain_hits[domain] += 1
                if matched_anchor is None:
                    matched_anchor = kw

    if not domain_hits:
        return None

    top_domain = max(domain_hits, key=domain_hits.get)
    confidence = min(1.0, domain_hits[top_domain] / 3)

    return {
        "top_domain": top_domain,
        "confidence": round(confidence, 2),
        "matched_anchor": matched_anchor
    }

# =========================================================
# MAIN MULTI-TIER ANALYSIS FUNCTION
# =========================================================
def run_full_multitier_analysis():
    # -----------------------------
    # LOAD FILES
    # -----------------------------
    df_reviews = pd.read_csv(REVIEWS_CSV)
    df_themes = pd.read_csv(THEMES_CSV)

    df_reviews.rename(columns={"rating": "rating_overall"}, inplace=True)
    
    with open(RULE_KEYWORDS_JSON, "r", encoding="utf-8") as f:
        RULE_KEYWORDS = json.load(f)

    with open(FOOD_ONTOLOGY_JSON, "r", encoding="utf-8") as f:
        FOOD_ONTOLOGY = json.load(f)

    # =====================================================
    # 🟦 TIER 1: VERBATIM DOMAIN DISTRIBUTION
    # =====================================================
    tier1_results = []

    for idx, text in enumerate(df_reviews[REVIEW_TEXT_COLUMN].astype(str)):
        result = rule_based_classify(text, RULE_KEYWORDS)
        if result:
            tier1_results.append({
                "review_id": idx,
                "domain": result["top_domain"]
            })

    # 🔥 SAFETY CHECK
    if not tier1_results:
        raise ValueError(
            "Tier-1 produced zero results. "
            "Check rule_keywords.json, review text column, or keyword coverage."
        )

    tier1_df = pd.DataFrame(tier1_results)

    tier1_counts = Counter(tier1_df["domain"])
    tier1_total = len(tier1_df)

    tier1_output = {
        "total_valid_reviews": tier1_total,
        "issue_distribution": [
            {
                "domain": domain,
                "count": count,
                "percentage": round((count / tier1_total) * 100, 2)
            }
            for domain, count in tier1_counts.most_common()
        ]
    }

    # IMPORTANT: FOOD_PROBLEM review IDs
    food_problem_review_ids = set(
        tier1_df[tier1_df["domain"] == "FOOD_PROBLEM"]["review_id"]
    )

    TOTAL_FOOD_PROBLEM_REVIEWS = len(food_problem_review_ids)

    # =====================================================
    # 🟨 TIER 2: FOOD QUALITY DIAGNOSTICS
    # =====================================================
    tier2_df = df_themes[
        (df_themes["theme"] == "food") &
        (df_themes["polarity"] == "negative") &
        (df_themes["subtheme"].isin(TIER2_FOOD_SUBTHEMES))
    ]

    tier2_review_ids = tier2_df["review_id"].unique()
    tier2_total_reviews = len(tier2_review_ids)

    tier2_distribution = (
        tier2_df
        .groupby("subtheme")["review_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    tier2_output = {
        "total_reviews": int(tier2_total_reviews),
        "percentage_of_food_problem_reviews": round(
            (tier2_total_reviews / TOTAL_FOOD_PROBLEM_REVIEWS) * 100, 2)
        if TOTAL_FOOD_PROBLEM_REVIEWS else 0,
        "quality_dimension_distribution": [
            {
                "concept": subtheme,
                "review_count": int(count),
                "percentage_within_tier_2": round(
                    (count / tier2_total_reviews) * 100, 2
                )
            }
            for subtheme, count in tier2_distribution.items()
        ],
        "interpretation": (
            "Tier-2 captures actionable food quality complaints describing how the food failed "
            "(taste, texture, freshness, preparation, quantity), independent of dish identity."
        )
    }

    # =====================================================
    # 🟥 TIER 3: DISH-LEVEL ROOT CAUSE ANALYSIS
    # =====================================================
    PHRASE_CANONICAL_MAP = {
        # Quantity / Portion
        "portion_size": {
            "small amount", "less amount", "very small amount",
            "too small", "too less", "should be more", "quantity less"
        },

        # Cooking quality
        "cooking_quality": {
            "burnt", "overcooked", "undercooked", "raw",
            "half cooked", "not cooked properly"
        },

        # Temperature
        "temperature": {
            "cold", "cold food", "served cold", "food cold"
        },

        # Texture
        "texture": {
            "soggy", "dry", "hard", "chewy", "rubbery"
        },

        # Freshness / Hygiene
        "freshness": {
            "stale", "stale food", "old food", "rotten",
            "spoiled", "smelly", "bad smell"
        },

        # Oil & grease
        "oiliness": {
            "oily", "greasy"
        },

        # Taste balance (not “taste” itself)
        "taste_balance": {
            "salty", "too salty", "saltless",
            "sweet", "too sweet",
            "too spicy", "extremely spicy", "no spice"
        },

        # Value (optional – you may drop later)
        "value": {
            "overpriced", "not worth", "not worth price", "waste money"
        }
    }
    PHRASE_TO_CONCEPT = {}
    for concept, phrases in PHRASE_CANONICAL_MAP.items():
        for p in phrases:
            PHRASE_TO_CONCEPT[p] = concept
    from collections import defaultdict

    def canonicalize_failure_breakdown(phrase_counts: dict):
        concept_counts = defaultdict(int)

        for phrase, count in phrase_counts.items():
            phrase_l = phrase.lower()

            if phrase_l in PHRASE_TO_CONCEPT:
                concept = PHRASE_TO_CONCEPT[phrase_l]
                concept_counts[concept] += count
            else:
                # keep uncategorized phrases as-is (optional)
                concept_counts["other"] += count

        return dict(concept_counts)

    food_neg = df_themes[
        (df_themes["theme"] == "food") &
        (df_themes["polarity"] == "negative") &
        (df_themes["rating"] <= 2)
    ]
    
    TOTAL_NEG_FOOD = len(food_neg)

    root_cause_counter = Counter()
    rating_impact = defaultdict(list)

    for _, row in food_neg.iterrows():
        key = f"{row['subtheme']}::{row['phrase']}"
        root_cause_counter[key] += 1
        rating_impact[key].append(row["rating"])

    TOP_ROOT_CAUSES = root_cause_counter.most_common(5)
    # =====================================================
    # 🟥 ROOT CAUSE SUMMARY (TOP 5 PHRASES)
    # =====================================================
    root_cause_summary = []

    for key, count in TOP_ROOT_CAUSES:
        subtheme, phrase = key.split("::")
        percentage = round((count / TOTAL_NEG_FOOD) * 100, 2)
        avg_rating = round(
            sum(rating_impact[key]) / len(rating_impact[key]), 2
        )

        root_cause_summary.append({
            "subtheme": subtheme,
            "phrase": phrase,
            "count": count,
            "percentage_of_food_complaints": percentage,
            "avg_rating": avg_rating
        })

    ALL_DISHES = []
    for group in FOOD_ONTOLOGY["food"]["dishes"].values():
        ALL_DISHES.extend(group)

    # =====================================================
    # 🟥 TIER 3: DISH-LEVEL ROOT CAUSE ANALYSIS (FIXED)
    # =====================================================
    dish_root_map = defaultdict(lambda: defaultdict(int))

    # 1️⃣ Populate raw phrase-level failures
    for _, row in food_neg.iterrows():
        review_text = df_reviews.loc[row["review_id"], REVIEW_TEXT_COLUMN].lower()
        for dish in ALL_DISHES:
            if dish in review_text:
                dish_root_map[dish][row["phrase"].lower()] += 1

    # 2️⃣ Canonicalize + score dishes
    dish_failure_scores = []

    for dish, phrase_counts in dish_root_map.items():
        total_failures = sum(phrase_counts.values())
        if total_failures < 3:
            continue

        canonical_breakdown = canonicalize_failure_breakdown(phrase_counts)

        dish_failure_scores.append({
            "dish": dish,
            "total_negative_mentions": total_failures,
            "failure_breakdown": canonical_breakdown
        })

    # 3️⃣ Sort & pick top 10 ONLY
    top_10_dish_failures = sorted(
        dish_failure_scores,
        key=lambda x: x["total_negative_mentions"],
        reverse=True
    )[:10]

    # =====================================================
    # FINAL TIER-3 OUTPUT
    # =====================================================
    tier3_output = {
        "total_negative_food_reviews": TOTAL_NEG_FOOD,
        "top_root_causes": root_cause_summary,
        "top_10_dish_failures": top_10_dish_failures
    }
    final_output={
        "tier_1": tier1_output,
        "tier_2": tier2_output,
        "tier_3": tier3_output
    }
    with open("multitier_analysis_output.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)
    print("Done with Verbatim Multilayer Analysis. Output saved to multitier_analysis_output.json")
    return final_output


# =========================================================
# ENTRY POINT
# =========================================================
    