interface Column<T> {
  key: string;
  header: string;
  render?: (item: T, key: string) => React.ReactNode;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: Array<{ key: string; data: T }>;
  maxHeight?: string;
}

export function DataTable<T>({ columns, data, maxHeight }: DataTableProps<T>) {
  return (
    <div className={`overflow-x-auto ${maxHeight ? `max-h-${maxHeight} overflow-y-auto` : ''}`} style={maxHeight ? { maxHeight } : undefined}>
      <table className="w-full border-collapse">
        <thead className="bg-[#0f1619]/80 border-b-2 border-[#2a3b42]/80 sticky top-0">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-[#94a3a8]">
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.key} className="border-b border-[#2a3b42]/40 hover:bg-[#182327]/60 transition-colors">
              {columns.map((col) => (
                <td key={col.key} className="p-3 text-sm text-[#e0e6e8]">
                  {col.render ? col.render(item.data, item.key) : String((item.data as Record<string, unknown>)[col.key] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
