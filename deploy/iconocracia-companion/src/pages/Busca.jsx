import { useState, useMemo } from 'react'
import { useCorpus } from '../hooks/useCorpus'
import { useFilters } from '../hooks/useFilters'
import SearchBar from '../components/SearchBar'
import Card from '../components/Card'
import ItemModal from '../components/ItemModal'

export default function Busca() {
  const { items, loading } = useCorpus()
  const { query, setQuery, regime, setRegime, pais, setPais, filtered, clearFilters } = useFilters(items)
  const [selected, setSelected] = useState(null)
  const [sortBy, setSortBy] = useState('relevancia')

  const regimes = useMemo(() => [...new Set(items.map(i => i.regime).filter(Boolean))].sort(), [items])
  const paises = useMemo(() => [...new Set(items.map(i => i.pais).filter(Boolean))].sort(), [items])

  const sorted = useMemo(() => {
    const arr = [...filtered]
    if (sortBy === 'data') arr.sort((a, b) => (parseInt(a.data_estimada) || 0) - (parseInt(b.data_estimada) || 0))
    if (sortBy === 'pais') arr.sort((a, b) => (a.pais_nome || '').localeCompare(b.pais_nome || ''))
    return arr
  }, [filtered, sortBy])

  if (loading) return <div className="flex items-center justify-center h-[60vh]"><p className="text-[#8B7355]">Carregando...</p></div>

  return (
    <div>
      <div className="px-8 py-6 border-b border-[rgba(139,115,85,0.25)] space-y-4">
        <SearchBar value={query} onChange={setQuery} placeholder="Buscar no corpus inteiro..." />
        <div className="flex flex-wrap items-center gap-3">
          <FilterSelect label="Regime" value={regime} options={regimes} onChange={setRegime} />
          <FilterSelect label="País" value={pais} options={paises} onChange={setPais} />
          <select value={sortBy} onChange={e => setSortBy(e.target.value)} className="text-xs border border-[rgba(139,115,85,0.25)] rounded px-2 py-1.5 bg-[#F5ECD6] text-[#3D2817]">
            <option value="relevancia">Relevância</option>
            <option value="data">Data</option>
            <option value="pais">País</option>
          </select>
          {(query || regime || pais) && (
            <button onClick={clearFilters} className="text-xs text-[#6B1E3A] hover:underline">Limpar filtros</button>
          )}
          <span className="text-xs text-[#8B7355] ml-auto">{sorted.length} resultados</span>
        </div>
      </div>
      <div className="px-8 py-6 columns-5 max-xl:columns-4 max-lg:columns-3 max-md:columns-2 gap-4">
        {sorted.map(item => (
          <Card key={item.id} item={item} onClick={setSelected} />
        ))}
        {sorted.length === 0 && (
          <div className="text-center py-16">
            <p className="font-serif text-lg text-[#8B7355]">Nenhum item encontrado</p>
            <button onClick={clearFilters} className="text-sm text-[#6B1E3A] hover:underline mt-2">Limpar filtros</button>
          </div>
        )}
      </div>
      {selected && <ItemModal item={selected} onClose={() => setSelected(null)} allItems={items} />}
    </div>
  )
}

function FilterSelect({ label, value, options, onChange }) {
  return (
    <div className="flex items-center gap-1">
      <span className="text-[10px] uppercase tracking-wider text-[#8B7355]">{label}:</span>
      <select value={value} onChange={e => onChange(e.target.value)} className="text-xs border border-[rgba(139,115,85,0.25)] rounded px-2 py-1.5 bg-[#F5ECD6] text-[#3D2817]">
        <option value="">Todos</option>
        {options.filter(Boolean).map(o => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  )
}
