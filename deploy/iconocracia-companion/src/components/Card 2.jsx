import ImageLoader from './ImageLoader'

const FLAGS = { FR:'🇫🇷', BR:'🇧🇷', UK:'🇬🇧', DE:'🇩🇪', IT:'🇮🇹', US:'🇺🇸', AT:'🇦🇹', PT:'🇵🇹', CH:'🇨🇭', GR:'🇬🇷', JP:'🇯🇵', ES:'🇪🇸', NL:'🇳🇱', BE:'🇧🇪', RU:'🇷🇺', AR:'🇦🇷' }

export default function Card({ item, onClick }) {
  return (
    <div
      onClick={() => onClick?.(item)}
      className="break-inside-avoid mb-4 bg-white border border-[#E8E3DC] rounded cursor-pointer
                 transition-all duration-300 ease-out
                 hover:border-[#C4A265] hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)]
                 hover:-translate-y-[3px] group relative overflow-hidden"
      role="button"
      tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && onClick?.(item)}
      aria-label={`${item.titulo}, ${item.pais_nome}, ${item.data_estimada}`}
    >
      <div className="relative overflow-hidden">
        <ImageLoader
          item={item}
          className="w-full block transition-transform duration-400 group-hover:scale-[1.03]"
        />
        {item.regime && (
          <span className="regime-badge absolute top-2 right-2">{item.regime}</span>
        )}
        <span className="catalog-no absolute bottom-2 left-2">{item.id}</span>
      </div>
      <div className="p-3">
        <p className="text-[13px] font-medium text-[#2C2C2C] leading-tight mb-1">{item.titulo}</p>
        <div className="flex items-center gap-1.5 text-[11px] text-[#9B8E82]">
          <span className="text-[13px]">{FLAGS[item.pais] || '🏳️'}</span>
          <span>{item.pais_nome}</span>
          <span className="text-[#E8E3DC]">·</span>
          <span className="font-mono text-[#A0522D]">{item.data_estimada}</span>
        </div>
      </div>
    </div>
  )
}
