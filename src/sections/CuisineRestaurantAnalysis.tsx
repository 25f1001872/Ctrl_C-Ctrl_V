import { ReportData } from "../types/report";

interface CuisineRestaurantAnalysisProps {
  data: ReportData;
}

export function CuisineRestaurantAnalysis({ data }: CuisineRestaurantAnalysisProps) {
  const byCuisine = data.stage_1_descriptive_statistics.by_cuisine;
  const byRestaurant = data.stage_1_descriptive_statistics.by_restaurant_top20;
  const topCuisines = data.stage_4_time_series.cuisine_overall_top || [];

  return (
    <section className="slide bg-gradient-to-b from-[#0f1619] to-[#182327] px-4 sm:px-6 lg:px-8 py-16">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <span className="metric-label">Segment Performance</span>
          <h2 className="text-3xl font-black tracking-tight mt-2 text-[#e0e6e8]">Cuisine & Restaurant Insights</h2>
        </div>

        {/* Top Cuisines */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h3 className="text-lg font-semibold mb-6 text-[#e0e6e8]">Top 5 Cuisines by Rating</h3>
            <div className="space-y-4">
              {topCuisines.slice(0, 5).map((cuisine) => (
                <div key={cuisine.primary_cuisine} className="flex items-center justify-between p-3 rounded-lg bg-[#0f1619]/50">
                  <div>
                    <p className="font-medium text-[#e0e6e8]">{cuisine.primary_cuisine}</p>
                    <p className="text-xs text-[#94a3a8]">{cuisine.rating_count.toLocaleString()} reviews</p>
                  </div>
                  <p className="text-lg font-bold text-[#0dccf2]">{cuisine.mean_rating.toFixed(2)}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h3 className="text-lg font-semibold mb-6 text-[#e0e6e8]">Full Cuisine Breakdown</h3>
            <div className="overflow-x-auto max-h-72 overflow-y-auto">
              <table className="w-full border-collapse">
                <thead className="bg-[#0f1619]/80 border-b-2 border-[#2a3b42]/80 sticky top-0">
                  <tr>
                    <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Cuisine</th>
                    <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Reviews</th>
                    <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Rating</th>
                    <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">CV (%)</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(byCuisine).map(([cuisine, stats]) => (
                    <tr key={cuisine} className="border-b border-[#2a3b42]/40 hover:bg-[#182327]/60 transition-colors">
                      <td className="p-3 text-sm text-[#e0e6e8]">{cuisine}</td>
                      <td className="p-3 text-sm text-[#e0e6e8]">{stats.count.toLocaleString()}</td>
                      <td className="p-3 text-sm text-[#0dccf2] font-semibold">{stats.mean.toFixed(2)}</td>
                      <td className="p-3 text-sm text-[#e0e6e8]">{stats["cv_%"].toFixed(1)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Top Restaurants */}
        <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
          <h3 className="text-lg font-semibold mb-6 text-[#e0e6e8]">Top 20 Restaurants by Review Volume</h3>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead className="bg-[#0f1619]/80 border-b-2 border-[#2a3b42]/80">
                <tr>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Restaurant</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Reviews</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Avg Rating</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Median</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Std Dev</th>
                  <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">Consistency</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(byRestaurant).slice(0, 20).map(([restaurant, stats]) => (
                  <tr key={restaurant} className="border-b border-[#2a3b42]/40 hover:bg-[#182327]/60 transition-colors">
                    <td className="p-3 text-sm text-[#e0e6e8]">{restaurant}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{stats.count.toLocaleString()}</td>
                    <td className="p-3 text-sm text-[#0dccf2] font-semibold">{stats.mean.toFixed(2)}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{stats.median.toFixed(2)}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">{stats.std.toFixed(2)}</td>
                    <td className="p-3 text-sm text-[#e0e6e8]">
                      <div className="progress-bar w-24">
                        <div
                          className="progress-fill"
                          style={{ width: `${Math.max(0, 100 - stats["cv_%"])}%` }}
                        />
                      </div>
                    </td>
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
