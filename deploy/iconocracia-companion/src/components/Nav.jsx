import { NavLink } from 'react-router-dom'

const TABS = [
  { to: '/', label: 'Atlas', end: true },
  { to: '/radiografia', label: 'Radiografia' },
  { to: '/busca', label: 'Busca' },
  { to: '/mapa', label: 'Mapa' },
  { to: '/glossario', label: 'Glossário' },
]

export default function Nav() {
  return (
    <header className="sticky top-0 z-30">
      <nav className="flex items-center justify-between px-8 py-5 bg-gradient-to-b from-[#2D4A3E] to-[#1F3A30] border-b border-[rgba(201,169,97,0.4)] shadow-[0_4px_24px_rgba(29,29,29,0.15)]">
        <div className="flex items-baseline gap-3">
          <span className="font-serif text-[22px] text-[#F5ECD6] tracking-[5px] leading-none">ICONOCRACIA</span>
          <span className="text-[8px] text-[rgba(201,169,97,0.8)] tracking-[3px] uppercase font-mono font-normal">atlas</span>
        </div>
        <div className="flex gap-1">
          {TABS.map(t => (
            <NavLink
              key={t.to}
              to={t.to}
              end={t.end}
              className={({ isActive }) =>
                `px-4 py-2 text-[13px] font-medium rounded-md transition-all duration-300
                 ${isActive
                   ? 'text-[#F5ECD6] bg-[rgba(201,169,97,0.2)] shadow-[inset_0_-2px_0_0_rgba(201,169,97,0.8)]'
                   : 'text-[rgba(245,236,214,0.7)] hover:text-[#F5ECD6] hover:bg-[rgba(255,255,255,0.08)]'
                 }`
              }
            >
              {t.label}
            </NavLink>
          ))}
        </div>
      </nav>
      <div className="gold-line" />
    </header>
  )
}
