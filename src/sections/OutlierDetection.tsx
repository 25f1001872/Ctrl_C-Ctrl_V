import { ReportData } from "../types/report";

interface OutlierDetectionProps {
  data: ReportData;
}

export function OutlierDetection({ data }: OutlierDetectionProps) {
  const outliers = data.stage_3_outlier_detection;
  const ratingIQR = outliers.rating_outliers_iqr;
  const likesIQR = outliers.likes_outliers_iqr;
  const ratingZ = outliers.rating_outliers_zscore;
  const likesZ = outliers.likes_outliers_zscore;
  const restRating = outliers.restaurant_rating_outliers_iqr;

  const getOutlierClass = (count: number) =>
    count === 0 ? 'bg-[#10b981]/10 text-[#10b981]' : 'bg-[#f59e0b]/10 text-[#f59e0b]';
  const qualityScore = Math.round(100 - outliers.anomaly_percentage);

  return (
    <section className="slide bg-gradient-to-b from-[#0f1619] to-[#182327] px-4 sm:px-6 lg:px-8 py-16">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <span className="metric-label">Data Quality</span>
          <h2 className="text-3xl font-black tracking-tight mt-2 text-[#e0e6e8]">Outlier Detection & Anomalies</h2>
        </div>

        {/* Outlier Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Rating Outliers (IQR) */}
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
              <span className="material-symbols-outlined text-[#ef4444]">warning</span>
              Rating Outliers (IQR)
            </h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Q1:</span>
                <span className="font-bold text-[#e0e6e8]">{ratingIQR.Q1.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Q3:</span>
                <span className="font-bold text-[#e0e6e8]">{ratingIQR.Q3.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">IQR:</span>
                <span className="font-bold text-[#0dccf2]">{ratingIQR.IQR.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Bounds:</span>
                <span className="font-bold text-[#ffb703]">[{ratingIQR.lower_bound.toFixed(2)}, {ratingIQR.upper_bound.toFixed(2)}]</span>
              </div>
              <hr className="border-[#2a3b42] my-2" />
              <div className={`flex justify-between p-2 rounded ${getOutlierClass(ratingIQR.outlier_count)}`}>
                <span>Outliers Found:</span>
                <span className="font-bold">{ratingIQR.outlier_count} ({ratingIQR.outlier_percentage.toFixed(2)}%)</span>
              </div>
            </div>
          </div>

          {/* Likes Outliers (IQR) */}
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
              <span className="material-symbols-outlined text-[#f59e0b]">thumb_up</span>
              Likes Outliers (IQR)
            </h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Q1:</span>
                <span className="font-bold text-[#e0e6e8]">{Math.round(likesIQR.Q1)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Q3:</span>
                <span className="font-bold text-[#e0e6e8]">{Math.round(likesIQR.Q3)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">IQR:</span>
                <span className="font-bold text-[#0dccf2]">{Math.round(likesIQR.IQR)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Bounds:</span>
                <span className="font-bold text-[#ffb703]">[{Math.round(likesIQR.lower_bound)}, {Math.round(likesIQR.upper_bound)}]</span>
              </div>
              <hr className="border-[#2a3b42] my-2" />
              <div className={`flex justify-between p-2 rounded ${getOutlierClass(likesIQR.outlier_count)}`}>
                <span>Outliers Found:</span>
                <span className="font-bold">{likesIQR.outlier_count.toLocaleString()} ({likesIQR.outlier_percentage.toFixed(2)}%)</span>
              </div>
            </div>
          </div>

          {/* Rating Outliers (Z-Score) */}
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
              <span className="material-symbols-outlined text-[#ef4444]">analytics</span>
              Rating Outliers (Z-Score)
            </h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Mean:</span>
                <span className="font-bold text-[#e0e6e8]">{ratingZ.mean.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Std Dev:</span>
                <span className="font-bold text-[#e0e6e8]">{ratingZ.std_dev.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Threshold:</span>
                <span className="font-bold text-[#0dccf2]">{ratingZ.threshold}</span>
              </div>
              <hr className="border-[#2a3b42] my-2" />
              <div className={`flex justify-between p-2 rounded ${getOutlierClass(ratingZ.outlier_count)}`}>
                <span>Outliers Found:</span>
                <span className="font-bold">{ratingZ.outlier_count} ({ratingZ.outlier_percentage.toFixed(2)}%)</span>
              </div>
            </div>
          </div>

          {/* Likes Outliers (Z-Score) */}
          <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
              <span className="material-symbols-outlined text-[#f59e0b]">trending_up</span>
              Likes Outliers (Z-Score)
            </h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Mean:</span>
                <span className="font-bold text-[#e0e6e8]">{Math.round(likesZ.mean)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Std Dev:</span>
                <span className="font-bold text-[#e0e6e8]">{Math.round(likesZ.std_dev)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94a3a8]">Threshold:</span>
                <span className="font-bold text-[#0dccf2]">{likesZ.threshold}</span>
              </div>
              <hr className="border-[#2a3b42] my-2" />
              <div className={`flex justify-between p-2 rounded ${getOutlierClass(likesZ.outlier_count)}`}>
                <span>Outliers Found:</span>
                <span className="font-bold">{likesZ.outlier_count} ({likesZ.outlier_percentage.toFixed(2)}%)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Restaurant Rating Outliers */}
        <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6 mb-8">
          <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
            <span className="material-symbols-outlined text-[#ffb703]">storefront</span>
            Restaurant-Level Rating Anomalies
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="p-3 rounded bg-[#0f1619]/50">
              <p className="text-[#94a3a8]">Q1</p>
              <p className="text-lg font-bold text-[#0dccf2]">{restRating.Q1.toFixed(3)}</p>
            </div>
            <div className="p-3 rounded bg-[#0f1619]/50">
              <p className="text-[#94a3a8]">Q3</p>
              <p className="text-lg font-bold text-[#0dccf2]">{restRating.Q3.toFixed(3)}</p>
            </div>
            <div className="p-3 rounded bg-[#0f1619]/50">
              <p className="text-[#94a3a8]">Bounds</p>
              <p className="text-sm font-bold text-[#ffb703]">[{restRating.lower_bound.toFixed(3)}, {restRating.upper_bound.toFixed(3)}]</p>
            </div>
            <div className={`p-3 rounded ${getOutlierClass(restRating.outlier_count)}`}>
              <p className="text-xs">Anomalies</p>
              <p className="text-lg font-bold">{restRating.outlier_count}</p>
            </div>
          </div>
        </div>

        {/* Anomaly Summary */}
        <div className="rounded-xl border border-[#2a3b42] bg-[#182327] p-6">
          <h4 className="font-semibold mb-4 flex items-center gap-2 text-[#e0e6e8]">
            <span className="material-symbols-outlined text-[#0dccf2]">flag</span>
            Multivariate Anomalies Summary
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-lg bg-[#0f1619]/50 text-center">
              <p className="text-3xl font-bold text-[#0dccf2]">{outliers.anomaly_count}</p>
              <p className="text-xs text-[#94a3a8] mt-1">Total Anomalies</p>
            </div>
            <div className="p-4 rounded-lg bg-[#0f1619]/50 text-center">
              <p className="text-3xl font-bold text-[#ffb703]">{outliers.anomaly_percentage.toFixed(2)}%</p>
              <p className="text-xs text-[#94a3a8] mt-1">of Dataset</p>
            </div>
            <div className="p-4 rounded-lg bg-[#0f1619]/50 text-center">
              <p className="text-3xl font-bold text-[#f59e0b]">{qualityScore}%</p>
              <p className="text-xs text-[#94a3a8] mt-1">Data Quality</p>
            </div>
            <div className="p-4 rounded-lg bg-[#0f1619]/50 text-center">
              <p className="text-3xl font-bold text-[#10b981]">✓</p>
              <p className="text-xs text-[#94a3a8] mt-1">Safe for Analysis</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
