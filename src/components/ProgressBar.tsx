interface ProgressBarProps {
  value: number;
  label?: string;
  sublabel?: string;
}

export function ProgressBar({ value, label, sublabel }: ProgressBarProps) {
  const clampedValue = Math.min(100, Math.max(0, value));
  
  return (
    <div>
      {label && <p className="text-sm text-[#94a3a8] mb-1">{label}</p>}
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${clampedValue}%` }} />
      </div>
      {sublabel && <p className="text-xs text-[#94a3a8] mt-1">{sublabel}</p>}
    </div>
  );
}
