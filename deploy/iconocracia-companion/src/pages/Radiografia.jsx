import { useCorpus } from '../hooks/useCorpus'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area } from 'recharts'
import { Activity } from 'lucide-react'

const COLORS = ['#6B1E3A', '#2D4A3E', '#C9A961', '#8B7355', '#A0522D', '#8B5CF6']
const REGIME_ORDER = ['Fundacional', 'Normativo', 'Militar', 'Contra-Alegoria']
const REGIME_DESC = {
  'Fundacional': 'Alegorias de fundação estatal e legitimação republicana',
  'Normativo': 'Alegorias de instituições jurídicas e ordem normativa',
  'Militar': 'Alegorias em contextos bélicos e de soberania armada',
  'Contra-Alegoria': 'Contestações, subversões e ausências alegóricas',
}

export default function Radiografia() {
  const { stats, loading } = useCorpus()
  if (loading) return <div className="flex items-center justify-center h-[60vh]"><p className="text-[#8B7355]">Analisando corpus...</p></div>

  const total = Object.values(stats.por_pais || {}).reduce((a, b) => a + b, 0)
  const paisData = Object.entries(stats.por_pais || {}).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count)
  const regimeData = REGIME_ORDER.filter(r => stats.por_regime?.[r]).map(r => ({ name: r, count: stats.por_regime[r] }))
  const suporteData = Object.entries(stats.por_suporte || {}).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count).slice(0, 8)
  const decadaData = Object.entries(stats.por_decada || {}).map(([name, count]) => ({ name, count })).sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
  const anosMin = decadaData.length > 0 ? decadaData[0].name : '—'
  const anosMax = decadaData.length > 0 ? decadaData[decadaData.length - 1].name : '—'

  return (
    <div className="anim-fade-in px-8 py-8 max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-10">
        <div className="flex items-center gap-3 mb-3">
          <Activity size={24} className="text-[#6B1E3A]" />
          <h1 className="font-serif text-4xl text-[#6B1E3A] tracking-wide">Radiografia</h1>
        </div>
        <p className="text-sm text-[#8B7355] leading-relaxed max-w-2xl">
          Análise quantitativa do corpus ICONOCRACIA — anatomia numérica de 265 alegorias jurídicas catalogadas.
        </p>
      </div>

      {/* Hero stats */}
      <div className="grid grid-cols-5 gap-4 mb-10">
        <BigStat label="Total" value={total} accent="text-[#6B1E3A]" />
        <BigStat label="Países" value={Object.keys(stats.por_pais || {}).length} accent="text-[#2D4A3E]" />
        <BigStat label="Regimes" value={Object.keys(stats.por_regime || {}).length} accent="text-[#A0522D]" />
        <BigStat label="Suportes" value={Object.keys(stats.por_suporte || {}).length} accent="text-[#C9A961]" />
        <BigStat label="Período" value={`${anosMin}–${anosMax}`} accent="text-[#8B7355]" small />
      </div>

      {regimeData.length > 0 && (
        <Section title="Distribuição por regime iconocrático" icon="⚖️">
          <div className="grid grid-cols-2 gap-8 items-center">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={regimeData} dataKey="count" nameKey="name" cx="50%" cy="50%" outerRadius={110} innerRadius={50}
                     label={({ name, count, percent }) => `${name} (${count})`}
                     stroke="rgba(232,220,196,0.5)" strokeWidth={2}>
                  {regimeData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip
                  contentStyle={{ background: '#F5ECD6', border: '1px solid rgba(139,115,85,0.3)', borderRadius: 8, fontSize: 12 }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="space-y-4">
              {regimeData.map((r, i) => (
                <div key={r.name} className="flex gap-3 items-start">
                  <div className="w-3 h-3 rounded-full mt-1 flex-shrink-0" style={{ background: COLORS[i % COLORS.length] }} />
                  <div>
                    <p className="font-semibold text-sm text-[#3D2817]">{r.name} <span className="text-[#C9A961]">({r.count})</span></p>
                    <p className="text-xs text-[#8B7355] leading-relaxed">{REGIME_DESC[r.name]}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Section>
      )}

      <div className="grid grid-cols-2 gap-6">
        {paisData.length > 0 && (
          <Section title="Distribuição por país" icon="🌍">
            <ResponsiveContainer width="100%" height={Math.max(250, paisData.length * 32)}>
              <BarChart data={paisData} layout="vertical" margin={{ left: 10 }}>
                <XAxis type="number" tick={{ fontSize: 11, fill: '#8B7355' }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="name" width={50} tick={{ fontSize: 11, fill: '#3D2817' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#F5ECD6', border: '1px solid rgba(139,115,85,0.3)', borderRadius: 8, fontSize: 12 }} />
                <Bar dataKey="count" fill="#6B1E3A" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Section>
        )}

        {decadaData.length > 0 && (
          <Section title="Distribuição temporal" icon="📅">
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={decadaData}>
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#8B7355' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#8B7355' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#F5ECD6', border: '1px solid rgba(139,115,85,0.3)', borderRadius: 8, fontSize: 12 }} />
                <defs>
                  <linearGradient id="goldGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#C9A961" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#C9A961" stopOpacity={0.05} />
                  </linearGradient>
                </defs>
                <Area type="monotone" dataKey="count" fill="url(#goldGrad)" stroke="#C9A961" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </Section>
        )}
      </div>

      {suporteData.length > 0 && (
        <Section title="Suportes mais frequentes" icon="🖼️" className="mt-6">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={suporteData}>
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#3D2817' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: '#8B7355' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background: '#F5ECD6', border: '1px solid rgba(139,115,85,0.3)', borderRadius: 8, fontSize: 12 }} />
              <Bar dataKey="count" fill="#2D4A3E" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Section>
      )}

      {total === 0 && (
        <p className="text-center text-[#8B7355] py-16 font-serif text-lg">Sem dados para exibir</p>
      )}
    </div>
  )
}

function BigStat({ label, value, accent, small }) {
  return (
    <div className="vintage-card rounded-lg p-5 text-center relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[#C9A961] to-transparent" />
      <p className={`font-serif ${small ? 'text-lg' : 'text-3xl'} ${accent} tracking-wide`}>{value}</p>
      <p className="text-[10px] text-[#8B7355] mt-1 tracking-[2px] uppercase">{label}</p>
    </div>
  )
}

function Section({ title, children, icon = '', className = '' }) {
  return (
    <section className={`vintage-card rounded-lg p-6 ${className}`}>
      <div className="flex items-center gap-2 mb-5 pb-3 border-b border-[rgba(139,115,85,0.2)]">
        {icon && <span className="text-lg opacity-60">{icon}</span>}
        <h2 className="font-serif text-xl text-[#6B1E3A] tracking-wide">{title}</h2>
      </div>
      {children}
    </section>
  )
}
