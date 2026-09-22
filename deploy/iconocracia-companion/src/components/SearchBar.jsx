import { Search, X } from 'lucide-react'

export default function SearchBar({ value, onChange, placeholder = 'Buscar por título, país, regime, suporte...' }) {
  return (
    <div className="flex-1 max-w-[480px] flex items-center gap-2 bg-[#F5ECD6] border border-[rgba(139,115,85,0.3)] rounded-lg px-3.5 py-2.5 transition-all duration-300 focus-within:border-[#6B1E3A] focus-within:shadow-[0_0_0_3px_rgba(107,30,58,0.12)]">
      <Search size={16} className="text-[#8B7355] flex-shrink-0 transition-colors duration-300 group-focus-within:text-[#6B1E3A]" />
      <input
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        className="border-none outline-none bg-transparent font-sans text-[13px] w-full text-[#3D2817] placeholder:text-[#8B7355]/70"
      />
      {value && (
        <button onClick={() => onChange('')} className="text-[#8B7355] hover:text-[#6B1E3A] transition-colors">
          <X size={14} />
        </button>
      )}
    </div>
  )
}
