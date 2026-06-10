const VIEWS = ['Mural', 'Temática', 'Temporal']

export default function ViewToggle({ current, onChange }) {
  return (
    <div className="flex gap-0.5 bg-[rgba(139,115,85,0.15)] rounded-lg p-1 border border-[rgba(139,115,85,0.2)]">
      {VIEWS.map(v => (
        <button
          key={v}
          onClick={() => onChange(v)}
          className={`px-4 py-2 rounded-md text-xs font-semibold tracking-wide transition-all duration-300
            ${current === v
              ? 'bg-[#6B1E3A] text-[#F5ECD6] shadow-[0_2px_8px_rgba(107,30,58,0.3),inset_0_1px_0_rgba(255,255,255,0.1)]'
              : 'text-[#3D2817] hover:text-[#6B1E3A] hover:bg-[rgba(245,236,214,0.6)]'
            }`}
        >
          {v}
        </button>
      ))}
    </div>
  )
}
