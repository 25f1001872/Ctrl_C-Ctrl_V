import { ReportData } from "../types/report";

interface TimeSeriesTrendsProps {
  data: ReportData;
}

export function TimeSeriesTrends({ data }: TimeSeriesTrendsProps) {
  const timeSeries = data.stage_4_time_series;
  const topDays = timeSeries.ts_daily_overall_top || [];
  const topMonths = timeSeries.ts_monthly_overall_top || [];
  const topCitiesMonthly = timeSeries.ts_monthly_by_city_top || [];

  return (
    <section className="slide bg-gradient-to-b from-[#182327] to-[#0f1619] px-4 sm:px-6 lg:px-8 py-16">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <span className="metric-label">Temporal Analysis</span>
          <h2 className="text-3xl font-black tracking-tight mt-2 text-[#e0e6e8]">Time Series Trends</h2>
        </div>

        {/* Top Days & Months by Rating */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-6 text-[#e0e6e8]">Top 5 Days by Average Rating</h4>
            <div className="space-y-3">
              {topDays.slice(0, 5).map((item, index) => {
                const date = Object.keys(item)[0];
                const stats = Object.values(item)[0];
                return (
                  <div key={index} className="p-3 rounded-lg bg-[#0f1619]/50 flex justify-between items-center">
                    <div>
                      <p className="font-medium text-[#e0e6e8]">{date}</p>
                      <p className="text-xs text-[#94a3a8]">{Math.round(stats.rating_count)} reviews</p>
                    </div>
                    <p className="text-lg font-bold text-[#10b981]">{stats.mean_rating.toFixed(2)} ★</p>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-6 text-[#e0e6e8]">Top 5 Months by Average Rating</h4>
            <div className="space-y-3">
              {topMonths.slice(0, 5).map((item, index) => {
                const month = Object.keys(item)[0];
                const stats = Object.values(item)[0];
                return (
                  <div key={index} className="p-3 rounded-lg bg-[#0f1619]/50 flex justify-between items-center">
                    <div>
                      <p className="font-medium text-[#e0e6e8]">{month}</p>
                      <p className="text-xs text-[#94a3a8]">{Math.round(stats.rating_count)} reviews</p>
                    </div>
                    <p className="text-lg font-bold text-[#10b981]">{stats.mean_rating.toFixed(2)} ★</p>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Top Cities by Month Table */}
        <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
          <h4 className="font-semibold mb-6 text-[#e0e6e8]">Top Cities by Month (Performance)</h4>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead className="bg-[#0f1619]/80 border-b-2 border-[#2a3b42]/80">
                <tr>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Month</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">City</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Avg Rating</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Review Count</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Avg Likes</th>
                </tr>
              </thead>
              <tbody>
                {topCitiesMonthly.map((item, index) => (
                  <tr key={index} className="border-b border-[#2a3b42]/40 hover:bg-[#182327]/60 transition-colors">
                    <td className="p-3 text-sm text-[#e0e6e8]">{item.created_at.substring(0, 7)}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{item.city}</td>
                    <td className="p-3 text-sm text-[#0dccf2] font-semibold">{item.mean_rating.toFixed(2)}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{item.rating_count.toLocaleString()}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{Math.round(item.mean_likes)}</td>
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
