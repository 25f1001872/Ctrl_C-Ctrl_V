import pandas as pd
import numpy as np
import json
from scipy import stats
from scipy.stats import f_oneway, ttest_ind, pearsonr
import warnings
warnings.filterwarnings('ignore')

INPUT_CSV = "final_reviews.csv"
OUTPUT_DIR = "./"

# ============ HELPER FUNCTIONS ============

def coefficient_of_variation(series):
    """Calculate CV = (std dev / mean) * 100"""
    return (series.std() / series.mean() * 100) if series.mean() != 0 else 0

def detect_outliers_iqr(series, column_name, multiplier=1.5):
    """Detect outliers using IQR method."""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    outliers = series[(series < lower_bound) | (series > upper_bound)]
    
    return {
        'column': column_name,
        'Q1': float(Q1),
        'Q3': float(Q3),
        'IQR': float(IQR),
        'lower_bound': float(lower_bound),
        'upper_bound': float(upper_bound),
        'outlier_count': int(len(outliers)),
        'outlier_percentage': float(len(outliers) / len(series) * 100),
#        'outlier_indices': list(outliers.index.tolist())
    }

def detect_outliers_zscore(series, column_name, threshold=3):
    """Detect outliers using Z-score method."""
    z_scores = np.abs(stats.zscore(series.dropna()))
    outliers_mask = z_scores > threshold
    outliers = series[series.index.isin(series.dropna().index[outliers_mask])]
    
    return {
        'column': column_name,
        'mean': float(series.mean()),
        'std_dev': float(series.std()),
        'threshold': threshold,
        'outlier_count': int(len(outliers)),
        'outlier_percentage': float(len(outliers) / len(series) * 100),
#        'outlier_indices': list(outliers.index.tolist())
    }

def eta_squared_from_groups(groups):
    all_vals = np.concatenate(groups)
    grand_mean = all_vals.mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_total = ((all_vals - grand_mean) ** 2).sum()
    return ss_between / ss_total if ss_total != 0 else 0.0

def interpret_eta_sq(eta):
    if eta < 0.01:
        return "Small"
    elif eta < 0.06:
        return "Medium"
    else:
        return "Large"

def signif_code(p):
    if p < 0.001:
        return "Yes***"
    elif p < 0.01:
        return "Yes**"
    elif p < 0.05:
        return "Yes*"
    else:
        return "No"

def interpret_cohens_d(d):
    ad = abs(d)
    if ad < 0.2:
        return "Negligible"
    elif ad < 0.5:
        return "Small"
    elif ad < 0.8:
        return "Medium"
    else:
        return "Large"

def interpret_r(r):
    ar = abs(r)
    if ar < 0.1:
        return "Negligible"
    elif ar < 0.3:
        return "Weak"
    elif ar < 0.5:
        return "Moderate"
    elif ar < 0.7:
        return "Strong"
    else:
        return "Very strong"

# ============ STAGE 1: DESCRIPTIVE STATISTICS ============

def stage_1_descriptive_stats(df):
    """Compute descriptive statistics."""
    print("\n" + "="*80)
    print("STAGE 1: DESCRIPTIVE STATISTICS")
    print("="*80)
    
    n_cities = df["city"].nunique()
    n_restaurants = df["restaurant_name"].nunique()
    
    do_city_stats = n_cities > 1
    do_restaurant_stats = n_restaurants > 1
    
    if n_cities == 1 and n_restaurants == 1:
        scope = "SINGLE_RESTAURANT_SINGLE_CITY"
    elif n_cities == 1 and n_restaurants > 1:
        scope = "MULTIPLE_RESTAURANTS_SINGLE_CITY"
    else:
        scope = "MULTIPLE_CITIES"
    
    result = {}
    
    # KEY INSIGHTS
    insights = {
        'Dataset Scope': scope,
        'Total Reviews': int(len(df)),
        'Date Range': f"{df['created_at'].min().date()} to {df['created_at'].max().date()}",
        'Number of Cities': int(n_cities),
        'Number of Restaurants': int(n_restaurants),
        'Number of Cuisines': int(df['primary_cuisine'].nunique()),
        'Number of Reviewers': int(df['reviewer_name'].nunique()),
        'Average Rating': round(df['rating_overall'].mean(), 2),
        'Median Rating': float(df['rating_overall'].median()),
        'Std Dev Rating': round(df['rating_overall'].std(), 2),
        'CV Rating (%)': round(coefficient_of_variation(df['rating_overall']), 2),
        'Rating Range': f"{df['rating_overall'].min():.0f} - {df['rating_overall'].max():.0f}",
        'Avg Likes per Review': round(df['like_count'].mean(), 2),
        'CV Likes (%)': round(coefficient_of_variation(df['like_count']), 2),
        'Reviews with Likes': f"{(df['like_count'] > 0).sum()} ({(df['like_count'] > 0).sum() / len(df) * 100:.1f}%)",
    }
    result['key_insights'] = insights
    print("\n✓ Key Insights computed")
    
    # OVERALL STATS
    numeric_cols = ['rating_overall', 'like_count', 'restaurant_overall_rating', 'restaurant_review_count']
    overall_stats = df[numeric_cols].describe().to_dict()
    cv_values = {col: coefficient_of_variation(df[col]) for col in numeric_cols}
    overall_stats['cv_%'] = cv_values
    result['overall_stats'] = overall_stats
    print("✓ Overall statistics computed")
    
    # BY CITY
    if do_city_stats:
        by_city_dict = {}
        by_city = df.groupby('city')['rating_overall'].agg(
            count='count',
            mean='mean',
            std='std',
            median='median',
            min='min',
            max='max'
        ).to_dict('index')
        for city, stats_dict in by_city.items():
            stats_dict['cv_%'] = (stats_dict['std'] / stats_dict['mean'] * 100) if stats_dict['mean'] != 0 else 0
        result['by_city'] = by_city
        print("✓ By-City statistics computed")
    else:
        result['by_city'] = "N/A (only 1 city)"
        print("✓ By-City statistics: skipped (only 1 city)")
    
    # BY CUISINE
    by_cuisine_dict = {}
    by_cuisine = df.groupby('primary_cuisine')['rating_overall'].agg(
        count='count',
        mean='mean',
        std='std',
        median='median',
        min='min',
        max='max'
    ).to_dict('index')
    for cuisine, stats_dict in by_cuisine.items():
        stats_dict['cv_%'] = (stats_dict['std'] / stats_dict['mean'] * 100) if stats_dict['mean'] != 0 else 0
    result['by_cuisine'] = by_cuisine
    print("✓ By-Cuisine statistics computed")
    
    # BY RESTAURANT (top 20)
    if do_restaurant_stats:
        by_restaurant_dict = {}
        by_restaurant = df.groupby('restaurant_name')['rating_overall'].agg(
            count='count',
            mean='mean',
            std='std',
            median='median',
            min='min',
            max='max'
        ).sort_values('count', ascending=False).head(20).to_dict('index')
        for rest, stats_dict in by_restaurant.items():
            stats_dict['cv_%'] = (stats_dict['std'] / stats_dict['mean'] * 100) if stats_dict['mean'] != 0 else 0
        result['by_restaurant_top20'] = by_restaurant
        print("✓ By-Restaurant statistics (top 20) computed")
    else:
        result['by_restaurant_top20'] = "N/A (only 1 restaurant)"
        print("✓ By-Restaurant statistics: skipped (only 1 restaurant)")
    
    return result

# ============ STAGE 2: ANOVA & STATISTICAL TESTS ============

def stage_2_statistical_tests(df):
    """Run ANOVA and statistical tests."""
    print("\n" + "="*80)
    print("STAGE 2: STATISTICAL TESTS (ANOVA, T-TEST, CORRELATION)")
    print("="*80)
    
    result = {}
    n_cities = df["city"].nunique()
    n_cuisines = df["primary_cuisine"].nunique()
    
    # ANOVA BY CITY
    if n_cities > 1:
        groups = []
        for city, g in df.groupby("city"):
            vals = g["rating_overall"].dropna().values
            if len(vals) >= 3:
                groups.append(vals)
        
        if len(groups) >= 2:
            f_city, p_city = f_oneway(*groups)
            eta_city = eta_squared_from_groups(groups)
            result['anova_by_city'] = {
                'F_statistic': float(f_city),
                'p_value': float(p_city),
                'eta_squared': float(eta_city),
                'effect_size': interpret_eta_sq(eta_city),
                'n_groups': len(groups),
                'significant': signif_code(p_city)
            }
            print("✓ ANOVA by City computed")
        else:
            result['anova_by_city'] = "N/A (not enough groups)"
            print("✓ ANOVA by City: skipped (insufficient data)")
    else:
        result['anova_by_city'] = "N/A (only 1 city)"
        print("✓ ANOVA by City: skipped (only 1 city)")
    
    # ANOVA BY CUISINE
    if n_cuisines > 1:
        groups = []
        for cuis, g in df.groupby("primary_cuisine"):
            vals = g["rating_overall"].dropna().values
            if len(vals) >= 3:
                groups.append(vals)
        
        if len(groups) >= 2:
            f_c, p_c = f_oneway(*groups)
            eta_c = eta_squared_from_groups(groups)
            result['anova_by_cuisine'] = {
                'F_statistic': float(f_c),
                'p_value': float(p_c),
                'eta_squared': float(eta_c),
                'effect_size': interpret_eta_sq(eta_c),
                'n_groups': len(groups),
                'significant': signif_code(p_c)
            }
            print("✓ ANOVA by Cuisine computed")
        else:
            result['anova_by_cuisine'] = "N/A (not enough groups)"
            print("✓ ANOVA by Cuisine: skipped (insufficient data)")
    else:
        result['anova_by_cuisine'] = "N/A (only 1 cuisine)"
        print("✓ ANOVA by Cuisine: skipped (only 1 cuisine)")
    
    # T-TEST: LIKES vs NO LIKES
    high = df[df["like_count"] > 0]["rating_overall"].dropna().values
    low = df[df["like_count"] == 0]["rating_overall"].dropna().values
    
    if len(high) >= 5 and len(low) >= 5:
        t_stat, p_t = ttest_ind(high, low, equal_var=False)
        s1, s2 = high.std(ddof=1), low.std(ddof=1)
        n1, n2 = len(high), len(low)
        pooled = np.sqrt(((n1 - 1)*s1**2 + (n2 - 1)*s2**2) / (n1 + n2 - 2)) if (n1+n2-2) > 0 else 0
        d = (high.mean() - low.mean()) / pooled if pooled != 0 else 0.0
        
        result['ttest_likes_comparison'] = {
            't_statistic': float(t_stat),
            'p_value': float(p_t),
            'cohens_d': float(d),
            'effect_size': interpret_cohens_d(d),
            'significant': signif_code(p_t),
            'mean_with_likes': float(high.mean()),
            'mean_without_likes': float(low.mean()),
            'mean_difference': float(high.mean() - low.mean()),
            'n_with_likes': int(n1),
            'n_without_likes': int(n2)
        }
        print("✓ T-Test (Likes comparison) computed")
    else:
        result['ttest_likes_comparison'] = "N/A (insufficient data)"
        print("✓ T-Test: skipped (insufficient data)")
    
    # CORRELATION: RATING vs LIKES
    corr_df = df[["rating_overall", "like_count"]].dropna()
    if len(corr_df) > 2:
        r, p_r = pearsonr(corr_df["rating_overall"], corr_df["like_count"])
        result['correlation_rating_likes'] = {
            'pearson_r': float(r),
            'p_value': float(p_r),
            'strength': interpret_r(r),
            'significant': signif_code(p_r)
        }
        print("✓ Correlation (Rating vs Likes) computed")
    else:
        result['correlation_rating_likes'] = "N/A (insufficient data)"
        print("✓ Correlation: skipped (insufficient data)")
    
    return result

# ============ STAGE 3: OUTLIER DETECTION ============

def stage_3_outlier_detection(df):
    """Detect outliers and anomalies."""
    print("\n" + "="*80)
    print("STAGE 3: OUTLIER DETECTION")
    print("="*80)
    
    result = {}
    
    # Statistical outliers
    rating_iqr = detect_outliers_iqr(df['rating_overall'], 'rating_overall')
    rating_zscore = detect_outliers_zscore(df['rating_overall'], 'rating_overall', threshold=3)
    likes_iqr = detect_outliers_iqr(df.loc[df['like_count'] > 0, 'like_count'],'like_count_nonzero')
    likes_zscore = detect_outliers_zscore(df['like_count'], 'like_count', threshold=3)
    rest_rating_iqr = detect_outliers_iqr(df['restaurant_overall_rating'], 'restaurant_overall_rating')
    
    result['rating_outliers_iqr'] = rating_iqr
    result['rating_outliers_zscore'] = rating_zscore
    result['likes_outliers_iqr'] = likes_iqr
    result['likes_outliers_zscore'] = likes_zscore
    result['restaurant_rating_outliers_iqr'] = rest_rating_iqr
    print("✓ Statistical outliers detected")
    
    # Realistic anomalies
    anomalies = []
    like_99_percentile = df['like_count'].quantile(0.99)
    
    for idx, row in df.iterrows():
        flags = []
        
        if row['restaurant_review_count'] >= 20:
            if abs(row['rating_overall'] - row['restaurant_overall_rating']) > 3:
                flags.append('outlier_vs_restaurant')
        
        if row['like_count'] > like_99_percentile and row['like_count'] > 5:
            flags.append('viral_engagement')
        
        # if idx in rating_iqr['outlier_indices'] and row['like_count'] > df['like_count'].quantile(0.75):
        #     flags.append('extreme_rating_with_engagement')
        
        if row['rating_overall'] <= 2 and row['like_count'] > like_99_percentile:
            flags.append('low_rating_high_engagement')
        
        if len(flags) >= 2 or (len(flags) == 1 and flags[0] in ['viral_engagement', 'low_rating_high_engagement']):
            anomalies.append({
                'reviewer_name': row['reviewer_name'],
                'rating_overall': float(row['rating_overall']),
                'like_count': int(row['like_count']),
                'restaurant_name': row['restaurant_name'],
                'anomaly_flags': '; '.join(flags),
                'flag_count': len(flags)
            })
    
    # result['multivariate_anomalies'] = anomalies 
    result['anomaly_count'] = len(anomalies)
    result['anomaly_percentage'] = round(len(anomalies) / len(df) * 100, 2)
    print(f"✓ Realistic anomalies detected: {len(anomalies)}")
    
    return result

# ============ STAGE 4: TIME SERIES ANALYSIS ============

def stage_4_time_series(df):
    """Build time series tables."""
    print("\n" + "=" * 80)
    print("STAGE 4: TIME SERIES ANALYSIS")
    print("=" * 80)

    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    result = {}

    # THIS LINE MUST COME BEFORE ANY resample() CALLS
    ts = df.set_index("created_at")

    # ================= DAILY: TOP 10 DAYS =================
    daily_agg = ts.resample("D").agg(
        mean_rating=("rating_overall", "mean"),
        median_rating=("rating_overall", "median"),
        rating_count=("rating_overall", "count"),
        mean_likes=("like_count", "mean"),
    )
    daily_agg["mean_rating_roll"] = daily_agg["mean_rating"].rolling(7, min_periods=1).mean()
    daily_agg["delta_rating"] = daily_agg["mean_rating"].diff()

    # drop days with no rating
    daily_agg = daily_agg.dropna(subset=["mean_rating"])

    # pick top 10 days by mean rating (you could also use "rating_count")
    top_n_days = 10
    daily_top = (
        daily_agg
        .nlargest(top_n_days, "mean_rating")
        .sort_index()  # sort back by date for nicer reading
    )

    daily_top_dict = daily_top.to_dict("index")
    daily_top_dict = {str(k): v for k, v in daily_top_dict.items()}
    result["ts_daily_overall_top"] = daily_top_dict
    print(f"✓ Daily time series (top {top_n_days} days by mean rating) computed")

    # ================= MONTHLY: TOP 3 MONTHS =================
    monthly_agg = ts.resample("ME").agg(
        mean_rating=("rating_overall", "mean"),
        median_rating=("rating_overall", "median"),
        rating_count=("rating_overall", "count"),
        mean_likes=("like_count", "mean"),
    )
    monthly_agg["mean_rating_roll"] = monthly_agg["mean_rating"].rolling(3, min_periods=1).mean()
    monthly_agg["delta_rating"] = monthly_agg["mean_rating"].diff()

    # drop months with no rating
    monthly_agg = monthly_agg.dropna(subset=["mean_rating"])

    top_n_months = 3
    monthly_top = (
        monthly_agg
        .nlargest(top_n_months, "mean_rating")
        .sort_index()
    )

    monthly_dict = monthly_top.to_dict("index")
    monthly_dict = {str(k): v for k, v in monthly_dict.items()}
    result["ts_monthly_overall_top"] = monthly_dict
    print(f"✓ Monthly time series (top {top_n_months} months by mean rating) computed")


    # Monthly by city: keep top 3 cities per month by mean rating
    monthly_city_full = (
        ts.groupby([pd.Grouper(freq="ME"), "city"])
          .agg(
              mean_rating=("rating_overall", "mean"),
              rating_count=("rating_overall", "count"),
              mean_likes=("like_count", "mean"),
          )
          .reset_index()
    )

    # optional: filter out city-month combos with very few reviews
    monthly_city_full = monthly_city_full[monthly_city_full["rating_count"] >= 5]

    # for each month, take top 3 cities by mean_rating
    monthly_city_top = (
        monthly_city_full
        .sort_values(["created_at", "mean_rating"], ascending=[True, False])
        .groupby("created_at")           # each month
        .head(3)                         # top 3 cities in that month
        .reset_index(drop=True)
    )

    result["ts_monthly_by_city_top"] = monthly_city_top.to_dict("records")
    print("✓ Monthly by city (top 3 cities per month) computed")


    # Top cuisines overall (across entire period)
    cuisine_summary = (
        df.groupby("primary_cuisine")["rating_overall"]
          .agg(mean_rating="mean", rating_count="count")
          .reset_index()
    )

    # keep only cuisines with enough reviews (tune this threshold if needed)
    cuisine_summary = cuisine_summary[cuisine_summary["rating_count"] >= 30]

    # top 5 cuisines by mean rating
    top_n_cuisines = 5
    top_cuisines = (
        cuisine_summary
        .nlargest(top_n_cuisines, "mean_rating")
        .reset_index(drop=True)
    )

    result["cuisine_overall_top"] = top_cuisines.to_dict("records")
    print(f"✓ Cuisine summary computed (top {top_n_cuisines} cuisines by mean rating)")


    return result

# ============ MAIN EXECUTION ============

def main():
    print("\n" + "="*80)
    print("COMBINED QUANTITATIVE ANALYSIS - ALL STAGES")
    print("="*80)
    
    # Load data
    df = pd.read_csv(INPUT_CSV)
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    print(f"\n✓ Loaded {len(df)} reviews")
    
    # Run all stages
    stage1_result = stage_1_descriptive_stats(df)
    stage2_result = stage_2_statistical_tests(df)
    stage3_result = stage_3_outlier_detection(df)
    stage4_result = stage_4_time_series(df)
    
    # Combine all results
    all_results = {
        'metadata': {
            'total_reviews': len(df),
            'date_range_start': str(df['created_at'].min().date()),
            'date_range_end': str(df['created_at'].max().date()),
            'generated_at': pd.Timestamp.now().isoformat()
        },
        'stage_1_descriptive_statistics': stage1_result,
        'stage_2_statistical_tests': stage2_result,
        'stage_3_outlier_detection': stage3_result,
        'stage_4_time_series': stage4_result
    }
    
    # Save JSON
    with open(f"{OUTPUT_DIR}report_data.json", 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print("\n✓ Saved report_data.json")
    
    # Save consolidated CSV
    with open(f"{OUTPUT_DIR}report_data_consolidated.csv", 'w') as f:
        f.write("# QUANTITATIVE ANALYSIS CONSOLIDATED REPORT\n")
        f.write(f"# Generated: {pd.Timestamp.now().isoformat()}\n")
        f.write(f"# Total Reviews: {len(df)}\n")
        f.write(f"# Date Range: {df['created_at'].min().date()} to {df['created_at'].max().date()}\n\n")
        
        # STAGE 1
        f.write("## STAGE 1: DESCRIPTIVE STATISTICS\n\n")
        f.write("### KEY INSIGHTS\n")
        insights_df = pd.DataFrame(list(stage1_result['key_insights'].items()), columns=['Metric', 'Value'])
        insights_df.to_csv(f, index=False)
        f.write("\n\n")
        
        f.write("### OVERALL STATISTICS\n")
        overall_df = pd.DataFrame(stage1_result['overall_stats']).T
        overall_df.to_csv(f)
        f.write("\n\n")
        
        if isinstance(stage1_result['by_city'], dict):
            f.write("### BY CITY STATISTICS\n")
            by_city_df = pd.DataFrame(stage1_result['by_city']).T
            by_city_df.to_csv(f)
            f.write("\n\n")
        else:
            f.write(f"### BY CITY STATISTICS: {stage1_result['by_city']}\n\n")
        
        f.write("### BY CUISINE STATISTICS\n")
        by_cuisine_df = pd.DataFrame(stage1_result['by_cuisine']).T
        by_cuisine_df.to_csv(f)
        f.write("\n\n")
        
        if isinstance(stage1_result['by_restaurant_top20'], dict):
            f.write("### BY RESTAURANT (TOP 20)\n")
            by_rest_df = pd.DataFrame(stage1_result['by_restaurant_top20']).T
            by_rest_df.to_csv(f)
            f.write("\n\n")
        else:
            f.write(f"### BY RESTAURANT: {stage1_result['by_restaurant_top20']}\n\n")
        
        # STAGE 2
        f.write("## STAGE 2: STATISTICAL TESTS\n\n")
        f.write("### ANOVA BY CITY\n")
        if isinstance(stage2_result['anova_by_city'], dict):
            anova_city_df = pd.DataFrame([stage2_result['anova_by_city']])
            anova_city_df.to_csv(f, index=False)
        else:
            f.write(stage2_result['anova_by_city'] + "\n")
        f.write("\n\n")
        
        f.write("### ANOVA BY CUISINE\n")
        if isinstance(stage2_result['anova_by_cuisine'], dict):
            anova_cuisine_df = pd.DataFrame([stage2_result['anova_by_cuisine']])
            anova_cuisine_df.to_csv(f, index=False)
        else:
            f.write(stage2_result['anova_by_cuisine'] + "\n")
        f.write("\n\n")
        
        f.write("### T-TEST: LIKES COMPARISON\n")
        if isinstance(stage2_result['ttest_likes_comparison'], dict):
            ttest_df = pd.DataFrame([stage2_result['ttest_likes_comparison']])
            ttest_df.to_csv(f, index=False)
        else:
            f.write(stage2_result['ttest_likes_comparison'] + "\n")
        f.write("\n\n")
        
        f.write("### CORRELATION: RATING VS LIKES\n")
        if isinstance(stage2_result['correlation_rating_likes'], dict):
            corr_df = pd.DataFrame([stage2_result['correlation_rating_likes']])
            corr_df.to_csv(f, index=False)
        else:
            f.write(stage2_result['correlation_rating_likes'] + "\n")
        f.write("\n\n")
        
        # STAGE 3
        f.write("## STAGE 3: OUTLIER DETECTION\n\n")
        f.write(f"### ANOMALY SUMMARY\n")
        f.write(f"Total Anomalies Found: {stage3_result['anomaly_count']}\n")
        f.write(f"Anomaly Percentage: {stage3_result['anomaly_percentage']}%\n\n")
        
        f.write("### RATING OUTLIERS (IQR)\n")
        rating_iqr_df = pd.DataFrame([stage3_result['rating_outliers_iqr']])
        rating_iqr_df.to_csv(f, index=False)
        f.write("\n\n")

        f.write("### RATING OUTLIERS (Z-SCORE)\n")
        rating_z_df = pd.DataFrame([stage3_result['rating_outliers_zscore']])
        rating_z_df.to_csv(f, index=False)
        f.write("\n\n")

        f.write("### LIKES OUTLIERS (IQR)\n")
        likes_iqr_df = pd.DataFrame([stage3_result['likes_outliers_iqr']])
        likes_iqr_df.to_csv(f, index=False)
        f.write("\n\n")

        f.write("### LIKES OUTLIERS (Z-SCORE)\n")
        likes_z_df = pd.DataFrame([stage3_result['likes_outliers_zscore']])
        likes_z_df.to_csv(f, index=False)
        f.write("\n\n")

        
        if stage3_result['multivariate_anomalies']:
            f.write("### MULTIVARIATE ANOMALIES (DETAILED)\n")
            anom_df = pd.DataFrame(stage3_result['multivariate_anomalies'])
            anom_df.to_csv(f, index=False)
            f.write("\n\n")
        
        # STAGE 4
        f.write("## STAGE 4: TIME SERIES ANALYSIS\n\n")
        f.write("### MONTHLY OVERALL TIME SERIES\n")
        monthly_df = pd.DataFrame(stage4_result['ts_monthly_overall']).T.reset_index()
        monthly_df.columns = ['date'] + monthly_df.columns.tolist()[1:]
        monthly_df.to_csv(f, index=False)
        f.write("\n\n")
        
        if stage4_result['ts_monthly_by_city']:
            f.write("### MONTHLY BY CITY\n")
            city_df = pd.DataFrame(stage4_result['ts_monthly_by_city'])
            city_df.to_csv(f, index=False)
            f.write("\n\n")
        
        if stage4_result['ts_monthly_by_cuisine']:
            f.write("### MONTHLY BY CUISINE\n")
            cuisine_df = pd.DataFrame(stage4_result['ts_monthly_by_cuisine'])
            cuisine_df.to_csv(f, index=False)
            f.write("\n\n")
    
    print("✓ Saved report_data_consolidated.csv")
    
    print("\n" + "="*80)
    print("✓ ALL ANALYSIS COMPLETE!")
    print("="*80)
    print("\nOutput Files:")
    print("  1. report_data.json - Structured JSON for programmatic access")
    print("  2. report_data_consolidated.csv - Human-readable consolidated table")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
