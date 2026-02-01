from .excel_ingestion import standardize_restaurant_reviews
from .quantitative_analysis import quantitative_analysis_runner
from .theme_extraction import run_theme_extraction
from .multilayer_verbatim_analysis import run_full_multitier_analysis
from .quote_relevance_scoring import generate_top_relevant_unique_quotes
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_STANDARD_CSV = BASE_DIR / "standardized_output.csv"
THEME_KEYWORDS_JSON = BASE_DIR / "flattened_keywords.json"
def run_all(INPUT_CSV):
    print("Starting the full analysis pipeline...")
    standardize_restaurant_reviews(INPUT_CSV, OUTPUT_STANDARD_CSV)
    
    print("✅ Standardization complete")
    # Performing quantitative analysis
    print("Starting quantitative analysis...")
    quantitative_results=quantitative_analysis_runner(OUTPUT_STANDARD_CSV)

    print("✅ Quantitative analysis complete")
    # Theme extraction

    print("Starting theme extraction...")
    theme_insights_results=run_theme_extraction(OUTPUT_STANDARD_CSV, THEME_KEYWORDS_JSON,"themes_test.csv")

    # Multilayer verbatim analysis
    qualitative_multilayer_verbatim=run_full_multitier_analysis()

    # Quote relevance scoring
    qualitative_quote_relevant=generate_top_relevant_unique_quotes(
        themes_csv="themes_test.csv",
        multitier_json="multitier_analysis_output.json",
        output_csv="top_relevant_unique_quotes.csv"
    )

    print("All processes completed successfully.")
    
    analysis_results = {
        "results":
        {
            "quantitative_analysis": quantitative_results,
            "theme_insights": theme_insights_results,
            "multilayer_verbatim_analysis": qualitative_multilayer_verbatim,
            "quote_relevance_scoring": qualitative_quote_relevant
        }
    }
    return analysis_results

