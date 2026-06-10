import { useState, useMemo } from 'react'
import { useCorpus } from '../hooks/useCorpus'
import { useFilters } from '../hooks/useFilters'
import SearchBar from '../components/SearchBar'
import ViewToggle from '../components/ViewToggle'
import Counter from '../components/Counter'
import Card from '../components/Card'
import ItemModal from '../components/ItemModal'

const REGIMES = ['Fundacional', 'Normativo', 'Militar', 'Contra-Alegoria']

const REGIME_ICONS = {
  'Fundacional': '🏛️',
  'Normativo': '⚖️',
  'Militar': '⚔️',
  'Contra-Alegoria': '🔥',
}

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
      <div className="flex flex-col items-center justify-center h-[70vh] gap-4">
        <div className="relative">
          <div className="w-16 h-16 border-2 border-[rgba(139,115,85,0.3)] border-t-[#C9A961] rounded-full animate-spin" />
          <div className="absolute inset-0 flex items-center justify-center text-xl">⚖️</div>
        </div>
        <p className="text-[#8B7355] font-serif text-lg tracking-wide">Carregando corpus...</p>
      </div>
    )
  }

  const total = items.length
  const isFiltered = query || filtered.length !== total

  return (
    <div className="anim-fade-in">
      {/* Glass toolbar */}
      <div className="glass-panel sticky top-[73px] z-20 mx-8 mt-4 mb-0 rounded-xl px-6 py-4 flex items-center gap-4">
        <SearchBar value={query} onChange={setQuery} />
        <ViewToggle current={view} onChange={setView} />
        <div className="ml-auto flex items-center gap-4">
          <Counter
            count={filtered.length}
            label={isFiltered ? 'resultados' : 'itens no corpus'}
          />
          {isFiltered && (
            <div className="h-5 w-px bg-[rgba(139,115,85,0.3)]" />
          )}
        </div>
      </div>

      {/* ─── MURAL VIEW ─── */}
      {view === 'Mural' && (
        <div className="px-8 pt-6 pb-12 columns-5 max-xl:columns-4 max-lg:columns-3 max-md:columns-2 gap-x-4 gap-y-0">
          {filtered.map(item => (
            <Card key={item.id} item={item} onClick={setSelected} />
          ))}
          {filtered.length === 0 && (
            <div className="col-span-full flex flex-col items-center justify-center py-20 anim-fade-in">
              <div className="text-5xl mb-4 opacity-30">🔍</div>
              <p className="font-serif text-xl text-[#8B7355]">Nenhum item encontrado</p>
              <p className="text-sm text-[#8B7355]/70 mt-1">Tente ajustar os filtros</p>
            </div>
          )}
        </div>
      )}

      {/* ─── THEMATIC VIEW ─── */}
      {view === 'Temática' && (
        <div className="px-8 pt-6 pb-12 space-y-12">
          {REGIMES.map(regime => (
            byRegime[regime]?.length > 0 && (
              <section key={regime} className="anim-fade-up">
                <div className="flex items-center gap-3 mb-5 pb-3 border-b border-[rgba(139,115,85,0.25)]">
                  <span className="text-2xl opacity-70">{REGIME_ICONS[regime]}</span>
                  <div>
                    <h2 className="font-serif text-2xl text-[#6B1E3A] tracking-wide">{regime}</h2>
                    <p className="text-[11px] text-[#8B7355] tracking-[2px] uppercase">{byRegime[regime].length} itens catalogados</p>
                  </div>
                </div>
                <div className="columns-5 max-xl:columns-4 max-lg:columns-3 max-md:columns-2 gap-x-4 gap-y-0">
                  {byRegime[regime].map(item => (
                    <Card key={item.id} item={item} onClick={setSelected} />
                  ))}
                </div>
              </section>
            )
          ))}
          {REGIMES.every(r => !byRegime[r]?.length) && (
            <div className="flex flex-col items-center justify-center py-20 anim-fade-in">
              <div className="text-5xl mb-4 opacity-30">🔍</div>
              <p className="font-serif text-xl text-[#8B7355]">Nenhum item encontrado</p>
            </div>
          )}
        </div>
      )}

      {/* ─── TEMPORAL VIEW ─── */}
      {view === 'Temporal' && (
        <div className="px-8 pt-6 pb-12">
          <div className="overflow-x-auto pb-4">
            <div className="flex gap-8 min-w-max">
              {byDecade.map(([decade, decadeItems]) => (
                <section key={decade} className="min-w-[300px] anim-fade-up">
                  <div className="mb-4 relative">
                    <div className="flex items-baseline gap-3 pb-3">
                      <h2 className="font-serif text-3xl text-[#6B1E3A] tracking-wide">{decade}</h2>
                      <div className="flex items-center gap-1">
                        <div className="w-2 h-2 rounded-full bg-[#C9A961]" />
                        <span className="text-[11px] text-[#8B7355] tracking-[2px] uppercase">{decadeItems.length} itens</span>
                      </div>
                    </div>
                    <div className="gold-line-vintage" />
                  </div>
                  <div className="columns-2 gap-3">
                    {decadeItems.map(item => (
                      <Card key={item.id} item={item} onClick={setSelected} />
                    ))}
                  </div>
                </section>
              ))}
              {byDecade.length === 0 && (
                <div className="flex flex-col items-center justify-center py-20 anim-fade-in">
                  <div className="text-5xl mb-4 opacity-30">📅</div>
                  <p className="font-serif text-xl text-[#8B7355]">Sem dados temporais</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ─── MODAL ─── */}
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
