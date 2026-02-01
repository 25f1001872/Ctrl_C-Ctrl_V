export interface ReportData {
  stage_1_descriptive_statistics: {
    key_insights: {
      "Total Reviews": number;
      "Number of Cities": number;
      "Number of Restaurants": number;
      "Number of Cuisines": number;
      "Number of Reviewers": number;
      "Date Range": string;
      "Average Rating": number;
      "Median Rating": number;
      "Std Dev Rating": number;
      "Avg Likes per Review": number;
      "Reviews with Likes": string;
      "CV Rating (%)": number;
      "CV Likes (%)": number;
    };
    overall_stats: {
      rating_overall: {
        count: number;
        mean: number;
        std: number;
        min: number;
        "25%": number;
        "50%": number;
        "75%": number;
        max: number;
      };
      like_count: {
        count: number;
        mean: number;
        std: number;
        min: number;
        "25%": number;
        "50%": number;
        "75%": number;
        max: number;
      };
    };
    by_city: Record<
      string,
      {
        count: number;
        mean: number;
        median: number;
        std: number;
        "cv_%": number;
      }
    >;
    by_cuisine: Record<
      string,
      {
        count: number;
        mean: number;
        median: number;
        std: number;
        "cv_%": number;
      }
    >;
    by_restaurant_top20: Record<
      string,
      {
        count: number;
        mean: number;
        median: number;
        std: number;
        "cv_%": number;
      }
    >;
  };
  stage_2_statistical_tests: {
    anova_by_city: {
      F_statistic: number;
      p_value: number;
      eta_squared: number;
      effect_size: string;
      significant: string;
    };
    anova_by_cuisine: {
      F_statistic: number;
      p_value: number;
      eta_squared: number;
      effect_size: string;
      significant: string;
    };
    ttest_likes_comparison: {
      mean_with_likes: number;
      mean_without_likes: number;
      mean_difference: number;
      t_statistic: number;
      p_value: number;
      cohens_d: number;
      significant: string;
      n_with_likes: number;
      n_without_likes: number;
    };
    correlation_rating_likes: {
      pearson_r: number;
      p_value: number;
      strength: string;
      significant: string;
    };
  };
  stage_3_outlier_detection: {
    rating_outliers_iqr: {
      Q1: number;
      Q3: number;
      IQR: number;
      lower_bound: number;
      upper_bound: number;
      outlier_count: number;
      outlier_percentage: number;
    };
    likes_outliers_iqr: {
      Q1: number;
      Q3: number;
      IQR: number;
      lower_bound: number;
      upper_bound: number;
      outlier_count: number;
      outlier_percentage: number;
    };
    rating_outliers_zscore: {
      mean: number;
      std_dev: number;
      threshold: number;
      outlier_count: number;
      outlier_percentage: number;
    };
    likes_outliers_zscore: {
      mean: number;
      std_dev: number;
      threshold: number;
      outlier_count: number;
      outlier_percentage: number;
    };
    restaurant_rating_outliers_iqr: {
      Q1: number;
      Q3: number;
      IQR: number;
      lower_bound: number;
      upper_bound: number;
      outlier_count: number;
    };
    anomaly_count: number;
    anomaly_percentage: number;
  };
  stage_4_time_series: {
    cuisine_overall_top?: Array<{
      primary_cuisine: string;
      rating_count: number;
      mean_rating: number;
    }>;
    ts_daily_overall_top?: Array<Record<string, { rating_count: number; mean_rating: number }>>;
    ts_monthly_overall_top?: Array<Record<string, { rating_count: number; mean_rating: number }>>;
    ts_monthly_by_city_top?: Array<{
      created_at: string;
      city: string;
      mean_rating: number;
      rating_count: number;
      mean_likes: number;
    }>;
  };
}
