import { useState, useEffect, useMemo } from 'react'

let cached = null

export function useCorpus() {
  const [data, setData] = useState(cached)
  const [loading, setLoading] = useState(!cached)

  useEffect(() => {
    if (cached) return
    import('../data/corpus.json').then(mod => {
      cached = mod.default
      setData(cached)
      setLoading(false)
    })
  }, [])

  const items = useMemo(() => data?.items || [], [data])
  const stats = useMemo(() => data?.stats || {}, [data])
  const meta = useMemo(() => data?.meta || {}, [data])

  return { items, stats, meta, loading }
}
