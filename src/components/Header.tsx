export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[#2a3b42] bg-[#0f1619]/95 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded bg-gradient-to-br from-[#0dccf2] to-blue-600 text-white shadow-[0_0_15px_-3px_rgba(13,204,242,0.15)]">
              <span className="material-symbols-outlined text-[20px]">analytics</span>
            </div>
            <span className="text-xl font-bold tracking-tight text-[#e0e6e8]">DineSight</span>
          </div>

          <div className="flex items-center gap-4">
            <button className="hidden sm:inline-flex items-center justify-center rounded-lg bg-[#0dccf2] px-4 py-2 text-sm font-bold text-[#0f1619] transition-all hover:bg-[#0ab8da] hover:shadow-[0_0_15px_-3px_rgba(13,204,242,0.15)]">
              <span className="material-symbols-outlined text-[18px] mr-2">download</span>
              Export Report
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
