import { useState, useMemo } from 'react'
import { useCorpus } from '../hooks/useCorpus'
import { useFilters } from '../hooks/useFilters'
import SearchBar from '../components/SearchBar'
import ViewToggle from '../components/ViewToggle'
import Counter from '../components/Counter'
import Card from '../components/Card'
import ItemModal from '../components/ItemModal'

const REGIMES = ['Fundacional', 'Normativo', 'Militar', 'Contra-Alegoria']

export default function Atlas() {
  const { items, loading } = useCorpus()
  const { query, setQuery, filtered } = useFilters(items)
  const [view, setView] = useState('Mural')
  const [selected, setSelected] = useState(null)

  const byRegime = useMemo(() => {
    const groups = {}
    filtered.forEach(i => {
      const r = i.regime || 'Outros'
      if (!groups[r]) groups[r] = []
      groups[r].push(i)
    })
    return groups
  }, [filtered])

  const byDecade = useMemo(() => {
    const groups = {}
    filtered.forEach(i => {
      if (!i.data_estimada) return
      const dec = Math.floor(parseInt(i.data_estimada) / 10) * 10
      if (isNaN(dec)) return
      const key = `${dec}s`
      if (!groups[key]) groups[key] = []
      groups[key].push(i)
    })
    return Object.entries(groups).sort(([a], [b]) => parseInt(a) - parseInt(b))
  }, [filtered])

  const selectedIdx = selected ? filtered.findIndex(i => i.id === selected.id) : -1

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <p className="text-[#9B8E82] font-serif text-lg animate-pulse">Carregando corpus...</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center gap-4 px-8 py-4 border-b border-[#E8E3DC]">
        <SearchBar value={query} onChange={setQuery} />
        <ViewToggle current={view} onChange={setView} />
        <Counter
          count={filtered.length}
          label={query || filtered.length !== items.length ? 'resultados' : 'itens no corpus'}
        />
      </div>

      {view === 'Mural' && (
        <div className="px-8 py-6 columns-5 max-xl:columns-4 max-lg:columns-3 max-md:columns-2 gap-4">
          {filtered.map(item => (
            <Card key={item.id} item={item} onClick={setSelected} />
          ))}
          {filtered.length === 0 && (
            <p className="text-center text-[#9B8E82] py-16 font-serif">Nenhum item encontrado</p>
          )}
        </div>
      )}

      {view === 'Temática' && (
        <div className="px-8 py-6 space-y-10">
          {REGIMES.map(regime => (
            byRegime[regime]?.length > 0 && (
              <section key={regime}>
                <div className="flex items-baseline gap-3 mb-4">
                  <h2 className="font-serif text-xl text-[#16213E]">{regime}</h2>
                  <span className="text-xs text-[#9B8E82]">{byRegime[regime].length} itens</span>
                </div>
                <div className="columns-5 max-xl:columns-4 max-lg:columns-3 max-md:columns-2 gap-4">
                  {byRegime[regime].map(item => (
                    <Card key={item.id} item={item} onClick={setSelected} />
                  ))}
                </div>
              </section>
            )
          ))}
          {REGIMES.every(r => !byRegime[r]?.length) && (
            <p className="text-center text-[#9B8E82] py-16 font-serif">Nenhum item encontrado</p>
          )}
        </div>
      )}

      {view === 'Temporal' && (
        <div className="px-8 py-6">
          <div className="overflow-x-auto">
            <div className="flex gap-8 min-w-max pb-4">
              {byDecade.map(([decade, decadeItems]) => (
                <section key={decade} className="min-w-[280px]">
                  <div className="flex items-baseline gap-2 mb-3 pb-2 border-b border-[#E8E3DC]">
                    <h2 className="font-serif text-lg text-[#16213E]">{decade}</h2>
                    <span className="text-[10px] text-[#9B8E82]">{decadeItems.length}</span>
                  </div>
                  <div className="columns-2 gap-3">
                    {decadeItems.map(item => (
                      <Card key={item.id} item={item} onClick={setSelected} />
                    ))}
                  </div>
                </section>
              ))}
              {byDecade.length === 0 && (
                <p className="text-center text-[#9B8E82] py-16 font-serif">Sem dados temporais</p>
              )}
            </div>
          </div>
        </div>
      )}

      {selected && (
        <ItemModal
          item={selected}
          onClose={() => setSelected(null)}
          onPrev={selectedIdx > 0 ? () => setSelected(filtered[selectedIdx - 1]) : null}
          onNext={selectedIdx < filtered.length - 1 ? () => setSelected(filtered[selectedIdx + 1]) : null}
          allItems={items}
        />
      )}
    </div>
  )
}
