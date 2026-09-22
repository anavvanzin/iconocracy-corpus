import { useState, useMemo } from 'react'

export function useFilters(items) {
  const [query, setQuery] = useState('')
  const [regime, setRegime] = useState('')
  const [pais, setPais] = useState('')

  const filtered = useMemo(() => {
    let result = items
    if (query) {
      const q = query.toLowerCase()
      result = result.filter(i =>
        (i.titulo || '').toLowerCase().includes(q) ||
        (i.pais_nome || '').toLowerCase().includes(q) ||
        (i.tags || []).some(t => t.toLowerCase().includes(q)) ||
        (i.suporte || '').toLowerCase().includes(q) ||
        (i.motivo || '').toLowerCase().includes(q)
      )
    }
    if (regime) result = result.filter(i => i.regime === regime)
    if (pais) result = result.filter(i => i.pais === pais)
    return result
  }, [items, query, regime, pais])

  const clearFilters = () => { setQuery(''); setRegime(''); setPais('') }

  return { query, setQuery, regime, setRegime, pais, setPais, filtered, clearFilters }
}
