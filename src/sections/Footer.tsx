interface FooterProps {
  totalReviews: number;
}

export function Footer({ totalReviews }: FooterProps) {
  return (
    <section className="slide bg-[#0f1619] px-4 sm:px-6 lg:px-8 py-16">
      <div className="max-w-7xl mx-auto text-center">
        <h3 className="text-2xl font-bold mb-4 text-[#e0e6e8]">Report Generation Complete</h3>
        <p className="text-[#94a3a8] mb-8">
          This quantitative analysis report was auto-generated from {totalReviews.toLocaleString()} reviews.
          <br />
          Generated at: {new Date().toLocaleString()}
        </p>
        <button className="inline-flex items-center justify-center rounded-lg bg-[#0dccf2] px-6 py-3 text-sm font-bold text-[#0f1619] transition-all hover:bg-[#0ab8da] hover:shadow-[0_0_15px_-3px_rgba(13,204,242,0.15)]">
          <span className="material-symbols-outlined text-[18px] mr-2">download</span>
          Download Full Report (PDF)
        </button>
      </div>
    </section>
  );
}
