interface StatCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  icon?: string;
}

export function StatCard({ label, value, subtitle, icon }: StatCardProps) {
  return (
    <div className="stat-card rounded-xl p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="metric-label">{label}</p>
          <p className="metric-value mt-2">{value}</p>
          {subtitle && <p className="text-sm text-[#94a3a8] mt-2">{subtitle}</p>}
        </div>
        {icon && (
          <span className="material-symbols-outlined text-4xl text-[#0dccf2] opacity-20">
            {icon}
          </span>
        )}
      </div>
    </div>
  );
}
