import { ReportData } from "../types/report";

interface DistributionAnalysisProps {
  data: ReportData;
}

function StatRow({ label, value, highlight = false }: { label: string; value: string | number; highlight?: boolean }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-sm text-[#94a3a8]">{label}</span>
      <span className={`text-lg font-bold ${highlight ? 'text-[#ffb703]' : 'text-[#0dccf2]'}`}>{value}</span>
    </div>
  );
}

export function DistributionAnalysis({ data }: DistributionAnalysisProps) {
  const overall = data.stage_1_descriptive_statistics.overall_stats;
  const byCity = data.stage_1_descriptive_statistics.by_city;

  return (
    <section className="slide bg-gradient-to-b from-[#182327] to-[#0f1619] px-4 sm:px-6 lg:px-8 py-16">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <span className="metric-label">Descriptive Statistics</span>
          <h2 className="text-3xl font-black tracking-tight mt-2 text-[#e0e6e8]">Distribution Analysis</h2>
        </div>

        {/* Rating & Likes Distribution */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h3 className="text-lg font-semibold mb-6 text-[#e0e6e8]">Rating Distribution</h3>
            <div className="space-y-4">
              <StatRow label="Min" value={overall.rating_overall.min.toFixed(2)} />
              <StatRow label="25th Percentile" value={overall.rating_overall["25%"].toFixed(2)} />
              <StatRow label="Median (50th)" value={overall.rating_overall["50%"].toFixed(2)} />
              <StatRow label="75th Percentile" value={overall.rating_overall["75%"].toFixed(2)} />
              <StatRow label="Max" value={overall.rating_overall.max.toFixed(2)} />
              <hr className="border-[#2a3b42] my-3" />
              <StatRow label="Mean" value={overall.rating_overall.mean.toFixed(2)} highlight />
              <div className="flex justify-between items-center">
                <span className="text-sm text-[#94a3a8]">Std Dev</span>
                <span className="text-lg font-bold text-[#f59e0b]">{overall.rating_overall.std.toFixed(2)}</span>
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h3 className="text-lg font-semibold mb-6 text-[#e0e6e8]">Engagement (Likes) Distribution</h3>
            <div className="space-y-4">
              <StatRow label="Min" value={Math.round(overall.like_count.min)} />
              <StatRow label="25th Percentile" value={Math.round(overall.like_count["25%"])} />
              <StatRow label="Median (50th)" value={Math.round(overall.like_count["50%"])} />
              <StatRow label="75th Percentile" value={Math.round(overall.like_count["75%"])} />
              <StatRow label="Max" value={Math.round(overall.like_count.max)} />
              <hr className="border-[#2a3b42] my-3" />
              <StatRow label="Mean" value={Math.round(overall.like_count.mean)} highlight />
              <div className="flex justify-between items-center">
                <span className="text-sm text-[#94a3a8]">Std Dev</span>
                <span className="text-lg font-bold text-[#f59e0b]">{Math.round(overall.like_count.std)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* City Performance Table */}
        <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
          <h3 className="text-lg font-semibold mb-6 text-[#e0e6e8]">Performance by City</h3>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead className="bg-[#0f1619]/80 border-b-2 border-[#2a3b42]/80">
                <tr>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">City</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Reviews</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Avg Rating</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Median</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Std Dev</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Variability (%)</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(byCity).map(([city, stats]) => (
                  <tr key={city} className="border-b border-[#2a3b42]/40 hover:bg-[#182327]/60 transition-colors">
                    <td className="p-3 text-sm text-[#e0e6e8]">{city}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{stats.count.toLocaleString()}</td>
                    <td className="p-3 text-sm text-[#0dccf2] font-semibold">{stats.mean.toFixed(2)}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{stats.median.toFixed(2)}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{stats.std.toFixed(2)}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{stats["cv_%"].toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
