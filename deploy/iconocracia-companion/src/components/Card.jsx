import ImageLoader from './ImageLoader'

const FLAGS = { FR:'🇫🇷', BR:'🇧🇷', UK:'🇬🇧', DE:'🇩🇪', IT:'🇮🇹', US:'🇺🇸', AT:'🇦🇹', PT:'🇵🇹', CH:'🇨🇭', GR:'🇬🇷', JP:'🇯🇵', ES:'🇪🇸', NL:'🇳🇱', BE:'🇧🇪', RU:'🇷🇺', AR:'🇦🇷' }

export default function Card({ item, onClick }) {
  return (
    <div
      onClick={() => onClick?.(item)}
      className="anim-card break-inside-avoid mb-4 vintage-card rounded cursor-pointer group relative overflow-hidden
                 transition-all duration-500 ease-out
                 hover:border-[rgba(107,30,58,0.4)]
                 hover:shadow-[0_12px_40px_rgba(61,40,23,0.12),0_0_0_1px_rgba(201,169,97,0.3)]
                 hover:-translate-y-1"
      role="button"
      tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && onClick?.(item)}
      aria-label={`${item.titulo}, ${item.pais_nome}, ${item.data_estimada}`}
    >
      {/* Gold accent line at top */}
      <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[#C9A961] to-[#6B1E3A] opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

      <div className="relative overflow-hidden">
        <ImageLoader
          item={item}
          className="w-full block transition-all duration-700 ease-out group-hover:scale-[1.05]"
        />
        {/* Subtle vignette overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-[rgba(61,40,23,0.3)] via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

        {item.regime && (
          <span className="regime-badge absolute top-2 right-2 opacity-80 group-hover:opacity-100 transition-opacity">{item.regime}</span>
        )}
        <span className="catalog-no absolute bottom-2 left-2">{item.id}</span>
      </div>
      <div className="p-3.5 relative">
        <p className="text-[13px] font-medium text-[#6B1E3A] leading-tight mb-1.5 group-hover:text-[#3D2817] transition-colors duration-300">{item.titulo}</p>
        <div className="flex items-center gap-1.5 text-[11px] text-[#8B7355]">
          <span className="text-[13px]">{FLAGS[item.pais] || '🏳️'}</span>
          <span>{item.pais_nome}</span>
          <span className="text-[#C9A961]">·</span>
          <span className="font-mono text-[10px] text-[#6B1E3A] tracking-wide">{item.data_estimada}</span>
        </div>
        {/* Bottom shimmer line */}
        <div className="absolute bottom-0 left-3 right-3 h-px bg-gradient-to-r from-transparent via-[rgba(201,169,97,0.5)] to-[rgba(107,30,58,0.3)] opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
      </div>
    </div>
  )
}
