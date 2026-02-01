import { StatCard } from "../components/StatCard";
import { ProgressBar } from "../components/ProgressBar";
import { ReportData } from "../types/report";

interface ExecutiveSummaryProps {
  data: ReportData;
}

export function ExecutiveSummary({ data }: ExecutiveSummaryProps) {
  const insights = data.stage_1_descriptive_statistics.key_insights;

  return (
    <section className="slide bg-gradient-to-b from-[#0f1619] to-[#182327] px-4 sm:px-6 lg:px-8 py-16">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <span className="metric-label">Report Overview</span>
          <h1 className="text-4xl sm:text-5xl font-black tracking-tight mt-2 mb-4 text-[#e0e6e8]">
            Quantitative Analysis
          </h1>
          <p className="text-lg text-[#94a3a8] max-w-2xl">
            Comprehensive statistical analysis of {insights["Total Reviews"].toLocaleString()} customer reviews across{" "}
            {insights["Number of Cities"]} cities, {insights["Number of Restaurants"]} restaurants, and{" "}
            {insights["Number of Cuisines"]} cuisines from {insights["Date Range"]}.
          </p>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <StatCard
            label="Total Reviews"
            value={insights["Total Reviews"].toLocaleString()}
            subtitle={insights["Date Range"]}
            icon="feed"
          />
          <StatCard
            label="Average Rating"
            value={insights["Average Rating"].toFixed(2)}
            subtitle="out of 5.0"
            icon="star"
          />
          <StatCard
            label="Avg Likes/Review"
            value={Math.round(insights["Avg Likes per Review"])}
            subtitle={insights["Reviews with Likes"]}
            icon="thumb_up"
          />
          <div className="stat-card rounded-xl p-6">
            <p className="metric-label">Median Rating</p>
            <p className="metric-value mt-2">{insights["Median Rating"]}</p>
            <p className="text-sm text-[#94a3a8] mt-2">{insights["Std Dev Rating"]} (std dev)</p>
          </div>
          <div className="stat-card rounded-xl p-6">
            <p className="metric-label">Geographic Coverage</p>
            <div className="flex gap-4 mt-3">
              <div>
                <p className="text-2xl font-bold text-[#0dccf2]">{insights["Number of Cities"]}</p>
                <p className="text-xs text-[#94a3a8]">Cities</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-[#0dccf2]">{insights["Number of Restaurants"]}</p>
                <p className="text-xs text-[#94a3a8]">Restaurants</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-[#0dccf2]">{insights["Number of Cuisines"]}</p>
                <p className="text-xs text-[#94a3a8]">Cuisines</p>
              </div>
            </div>
          </div>
          <StatCard
            label="Reviewer Base"
            value={insights["Number of Reviewers"].toLocaleString()}
            subtitle="Unique reviewers"
          />
        </div>

        {/* Variability Insights */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h3 className="text-lg font-semibold mb-4 text-[#e0e6e8]">Rating Consistency</h3>
            <ProgressBar
              value={Math.min(100, Math.round(insights["CV Rating (%)"]))}
              label="Coefficient of Variation (Rating)"
              sublabel={`${insights["CV Rating (%)"].toFixed(1)}% variability`}
            />
          </div>
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h3 className="text-lg font-semibold mb-4 text-[#e0e6e8]">Engagement Spread</h3>
            <ProgressBar
              value={Math.min(100, Math.round(insights["CV Likes (%)"]))}
              label="Coefficient of Variation (Likes)"
              sublabel={`${insights["CV Likes (%)"].toFixed(1)}% variability`}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
