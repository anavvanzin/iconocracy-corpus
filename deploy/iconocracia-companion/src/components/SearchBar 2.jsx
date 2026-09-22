import { Search, X } from 'lucide-react'

export default function SearchBar({ value, onChange, placeholder = 'Buscar por título, país, regime, suporte...' }) {
  return (
    <div className="flex-1 max-w-[480px] flex items-center gap-2 bg-white border border-[#E8E3DC] rounded-lg px-3.5 py-2 transition-colors focus-within:border-[#C4A265]">
      <Search size={16} className="text-[#9B8E82] flex-shrink-0" />
      <input
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        className="border-none outline-none bg-transparent font-sans text-sm w-full text-[#2C2C2C] placeholder:text-[#9B8E82]"
      />
      {value && (
        <button onClick={() => onChange('')} className="text-[#9B8E82] hover:text-[#2C2C2C]">
          <X size={14} />
        </button>
      )}
    </div>
  )
}
