import { ReportData } from "../types/report";

interface StatisticalTestsProps {
  data: ReportData;
}

function StatItem({ label, value, className = "" }: { label: string; value: string | number; className?: string }) {
  return (
    <div className="flex justify-between">
      <span className="text-[#94a3a8]">{label}</span>
      <span className={`font-bold ${className || 'text-[#0dccf2]'}`}>{value}</span>
    </div>
  );
}

export function StatisticalTests({ data }: StatisticalTestsProps) {
  const anovaCity = data.stage_2_statistical_tests.anova_by_city;
  const anovaCuisine = data.stage_2_statistical_tests.anova_by_cuisine;
  const ttestLikes = data.stage_2_statistical_tests.ttest_likes_comparison;
  const corrRatingLikes = data.stage_2_statistical_tests.correlation_rating_likes;

  const getSigClass = (pValue: number) => (pValue < 0.05 ? 'text-[#10b981]' : 'text-[#f59e0b]');
  const getStrengthDesc = (r: number) => {
    const absR = Math.abs(r);
    if (absR < 0.1) return 'negligible';
    if (absR < 0.3) return 'weak';
    if (absR < 0.5) return 'moderate';
    if (absR < 0.7) return 'strong';
    return 'very strong';
  };

  return (
    <section className="slide bg-gradient-to-b from-[#182327] to-[#0f1619] px-4 sm:px-6 lg:px-8 py-16">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <span className="metric-label">Statistical Analysis</span>
          <h2 className="text-3xl font-black tracking-tight mt-2 text-[#e0e6e8]">Hypothesis Testing & Correlations</h2>
        </div>

        {/* ANOVA Tests */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* ANOVA by City */}
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
              <span className="material-symbols-outlined text-[#0dccf2]">location_city</span>
              ANOVA: City Effect
            </h4>
            <div className="space-y-3 text-sm">
              <StatItem label="F-Statistic:" value={anovaCity.F_statistic.toFixed(4)} />
              <StatItem label="P-Value:" value={anovaCity.p_value.toFixed(4)} className={getSigClass(anovaCity.p_value)} />
              <StatItem label="Eta Squared:" value={anovaCity.eta_squared.toFixed(6)} className="text-[#ffb703]" />
              <StatItem label="Effect Size:" value={anovaCity.effect_size} className="text-[#e0e6e8]" />
              <hr className="border-[#2a3b42] my-2" />
              <div className="flex justify-between p-2 rounded bg-[#0f1619]/50">
                <span className="text-[#e0e6e8]">Significant?</span>
                <span className={`font-bold ${getSigClass(anovaCity.p_value)}`}>{anovaCity.significant}</span>
              </div>
            </div>
          </div>

          {/* ANOVA by Cuisine */}
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
              <span className="material-symbols-outlined text-[#0dccf2]">restaurant_menu</span>
              ANOVA: Cuisine Effect
            </h4>
            <div className="space-y-3 text-sm">
              <StatItem label="F-Statistic:" value={anovaCuisine.F_statistic.toFixed(4)} />
              <StatItem label="P-Value:" value={anovaCuisine.p_value.toFixed(5)} className={getSigClass(anovaCuisine.p_value)} />
              <StatItem label="Eta Squared:" value={anovaCuisine.eta_squared.toFixed(6)} className="text-[#ffb703]" />
              <StatItem label="Effect Size:" value={anovaCuisine.effect_size} className="text-[#e0e6e8]" />
              <hr className="border-[#2a3b42] my-2" />
              <div className="flex justify-between p-2 rounded bg-[#0f1619]/50">
                <span className="text-[#e0e6e8]">Significant?</span>
                <span className={`font-bold ${getSigClass(anovaCuisine.p_value)}`}>{anovaCuisine.significant}</span>
              </div>
            </div>
          </div>
        </div>

        {/* T-Test & Correlation */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* T-Test: Likes Comparison */}
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
              <span className="material-symbols-outlined text-[#0dccf2]">compare_arrows</span>
              T-Test: Likes Impact
            </h4>
            <div className="space-y-3 text-sm">
              <StatItem
                label={`With Likes (n=${ttestLikes.n_with_likes.toLocaleString()}):`}
                value={`${ttestLikes.mean_with_likes.toFixed(2)} avg`}
              />
              <StatItem
                label={`Without Likes (n=${ttestLikes.n_without_likes.toLocaleString()}):`}
                value={`${ttestLikes.mean_without_likes.toFixed(2)} avg`}
                className="text-[#f59e0b]"
              />
              <StatItem label="Difference:" value={ttestLikes.mean_difference.toFixed(2)} className="text-[#e0e6e8]" />
              <hr className="border-[#2a3b42] my-2" />
              <StatItem label="T-Statistic:" value={ttestLikes.t_statistic.toFixed(4)} className="text-[#e0e6e8]" />
              <StatItem label="Cohen's d:" value={ttestLikes.cohens_d.toFixed(4)} className="text-[#ffb703]" />
              <div className="flex justify-between p-2 rounded bg-[#0f1619]/50">
                <span className="text-[#e0e6e8]">Significant?</span>
                <span className={`font-bold ${getSigClass(ttestLikes.p_value)}`}>{ttestLikes.significant}</span>
              </div>
            </div>
          </div>

          {/* Correlation */}
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
              <span className="material-symbols-outlined text-[#0dccf2]">scatter_plot</span>
              Correlation: Rating vs Likes
            </h4>
            <div className="space-y-3 text-sm">
              <StatItem label="Pearson r:" value={corrRatingLikes.pearson_r.toFixed(4)} />
              <StatItem label="P-Value:" value={corrRatingLikes.p_value.toFixed(5)} className={getSigClass(corrRatingLikes.p_value)} />
              <StatItem label="Strength:" value={corrRatingLikes.strength} className="text-[#e0e6e8]" />
              <hr className="border-[#2a3b42] my-2" />
              <div className="p-3 rounded bg-[#0f1619]/50">
                <p className="text-xs text-[#94a3a8]">
                  Interpretation: There is a <strong className="text-[#e0e6e8]">{getStrengthDesc(corrRatingLikes.pearson_r)}</strong>{" "}
                  relationship between ratings and engagement (likes).
                </p>
              </div>
              <div className="flex justify-between p-2 rounded bg-[#0f1619]/50">
                <span className="text-[#e0e6e8]">Statistically Significant?</span>
                <span className={`font-bold ${getSigClass(corrRatingLikes.p_value)}`}>{corrRatingLikes.significant}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
