import { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { ExecutiveSummary } from "./sections/ExecutiveSummary";
import { DistributionAnalysis } from "./sections/DistributionAnalysis";
import { CuisineRestaurantAnalysis } from "./sections/CuisineRestaurantAnalysis";
import { StatisticalTests } from "./sections/StatisticalTests";
import { OutlierDetection } from "./sections/OutlierDetection";
import { TimeSeriesTrends } from "./sections/TimeSeriesTrends";
import { Footer } from "./sections/Footer";
import { ReportData } from "./types/report";
import { sampleReportData } from "./data/sampleData";

type LoadingState = "loading" | "loaded" | "error";

export function App() {
  const [data, setData] = useState<ReportData | null>(null);
  const [loadingState, setLoadingState] = useState<LoadingState>("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [jsonInput, setJsonInput] = useState<string>("");
  const [showJsonInput, setShowJsonInput] = useState(false);

  useEffect(() => {
    // Try to fetch report_data.json from public folder
    fetch("/report_data.json")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        return res.json();
      })
      .then((jsonData: ReportData) => {
        setData(jsonData);
        setLoadingState("loaded");
      })
      .catch((err) => {
        console.warn("Could not load report_data.json:", err.message);
        // Fall back to sample data
        setData(sampleReportData);
        setLoadingState("loaded");
        setErrorMessage("Using sample data. Place your report_data.json in the public folder to use your own data.");
      });
  }, []);

  const handleJsonSubmit = () => {
    try {
      const parsed = JSON.parse(jsonInput);
      setData(parsed);
      setLoadingState("loaded");
      setErrorMessage("");
      setShowJsonInput(false);
    } catch (err) {
      setErrorMessage("Invalid JSON format. Please check your input.");
    }
  };

  const handleUseSampleData = () => {
    setData(sampleReportData);
    setLoadingState("loaded");
    setErrorMessage("");
    setShowJsonInput(false);
  };

  if (loadingState === "loading") {
    return (
      <div className="min-h-screen bg-[#0f1619] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-12 h-12 border-4 border-[#0dccf2] border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-[#94a3a8]">Loading report data...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-[#0f1619] flex items-center justify-center p-4">
        <div className="max-w-2xl w-full bg-[#182327] rounded-xl border border-[#2a3b42] p-8">
          <h2 className="text-2xl font-bold text-[#e0e6e8] mb-4">Load Report Data</h2>
          <p className="text-[#94a3a8] mb-6">
            No report_data.json found. You can either paste your JSON data below or use sample data.
          </p>
          
          {errorMessage && (
            <div className="bg-[#ef4444]/10 border border-[#ef4444]/30 rounded-lg p-3 mb-4">
              <p className="text-[#ef4444] text-sm">{errorMessage}</p>
            </div>
          )}

          {showJsonInput ? (
            <>
              <textarea
                className="w-full h-64 bg-[#0f1619] border border-[#2a3b42] rounded-lg p-4 text-[#e0e6e8] text-sm font-mono resize-none focus:outline-none focus:border-[#0dccf2]"
                placeholder="Paste your JSON data here..."
                value={jsonInput}
                onChange={(e) => setJsonInput(e.target.value)}
              />
              <div className="flex gap-4 mt-4">
                <button
                  onClick={handleJsonSubmit}
                  className="flex-1 bg-[#0dccf2] text-[#0f1619] font-bold py-3 rounded-lg hover:bg-[#0ab8da] transition-colors"
                >
                  Load JSON
                </button>
                <button
                  onClick={() => setShowJsonInput(false)}
                  className="flex-1 bg-[#2a3b42] text-[#e0e6e8] font-bold py-3 rounded-lg hover:bg-[#3c525b] transition-colors"
                >
                  Cancel
                </button>
              </div>
            </>
          ) : (
            <div className="flex gap-4">
              <button
                onClick={() => setShowJsonInput(true)}
                className="flex-1 bg-[#0dccf2] text-[#0f1619] font-bold py-3 rounded-lg hover:bg-[#0ab8da] transition-colors"
              >
                Paste JSON Data
              </button>
              <button
                onClick={handleUseSampleData}
                className="flex-1 bg-[#2a3b42] text-[#e0e6e8] font-bold py-3 rounded-lg hover:bg-[#3c525b] transition-colors"
              >
                Use Sample Data
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0f1619] text-[#e0e6e8] antialiased overflow-x-hidden selection:bg-[#0dccf2]/30 selection:text-[#0dccf2]">
      <Header />
      
      {errorMessage && (
        <div className="bg-[#ffb703]/10 border-b border-[#ffb703]/30 px-4 py-2">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <p className="text-[#ffb703] text-sm">{errorMessage}</p>
            <button
              onClick={() => setShowJsonInput(true)}
              className="text-[#0dccf2] text-sm hover:underline"
            >
              Load Custom Data
            </button>
          </div>
        </div>
      )}

      {showJsonInput && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
          <div className="max-w-2xl w-full bg-[#182327] rounded-xl border border-[#2a3b42] p-8">
            <h2 className="text-2xl font-bold text-[#e0e6e8] mb-4">Load Custom Report Data</h2>
            <textarea
              className="w-full h-64 bg-[#0f1619] border border-[#2a3b42] rounded-lg p-4 text-[#e0e6e8] text-sm font-mono resize-none focus:outline-none focus:border-[#0dccf2]"
              placeholder="Paste your JSON data here..."
              value={jsonInput}
              onChange={(e) => setJsonInput(e.target.value)}
            />
            <div className="flex gap-4 mt-4">
              <button
                onClick={handleJsonSubmit}
                className="flex-1 bg-[#0dccf2] text-[#0f1619] font-bold py-3 rounded-lg hover:bg-[#0ab8da] transition-colors"
              >
                Load JSON
              </button>
              <button
                onClick={() => setShowJsonInput(false)}
                className="flex-1 bg-[#2a3b42] text-[#e0e6e8] font-bold py-3 rounded-lg hover:bg-[#3c525b] transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <main className="flex-grow overflow-y-auto scroll-smooth" style={{ scrollSnapType: "y mandatory" }}>
        <ExecutiveSummary data={data} />
        <DistributionAnalysis data={data} />
        <CuisineRestaurantAnalysis data={data} />
        <StatisticalTests data={data} />
        <OutlierDetection data={data} />
        <TimeSeriesTrends data={data} />
        <Footer totalReviews={data.stage_1_descriptive_statistics.key_insights["Total Reviews"]} />
      </main>
    </div>
  );
}
