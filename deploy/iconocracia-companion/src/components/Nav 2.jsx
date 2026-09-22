import { NavLink } from 'react-router-dom'

const TABS = [
  { to: '/', label: 'Atlas', end: true },
  { to: '/mapa', label: 'Mapa' },
  { to: '/busca', label: 'Busca' },
  { to: '/stats', label: 'Stats' },
  { to: '/diario', label: 'Diário' },
]

export default function Nav() {
  return (
    <nav className="sticky top-0 z-30 flex items-center justify-between px-8 py-4 bg-[#FAF7F2] border-b border-[#E8E3DC]">
      <div className="flex items-baseline gap-3">
        <span className="font-serif text-2xl text-[#16213E] tracking-widest">ICONOCRACIA</span>
        <span className="text-xs text-[#A0522D] tracking-wider font-sans">atlas</span>
      </div>
      <div className="flex gap-1">
        {TABS.map(t => (
          <NavLink
            key={t.to}
            to={t.to}
            end={t.end}
            className={({ isActive }) =>
              `px-4 py-2 text-[13px] font-medium rounded-md transition-all
               ${isActive
                 ? 'text-[#16213E] bg-[#16213E]/[0.08]'
                 : 'text-[#9B8E82] hover:text-[#2C2C2C] hover:bg-black/[0.04]'
               }`
            }
          >
            {t.label}
          </NavLink>
        ))}
      </div>
    </nav>
  )
}
