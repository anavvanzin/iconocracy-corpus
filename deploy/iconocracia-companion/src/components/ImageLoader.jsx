import { useState } from 'react'

export default function ImageLoader({ item, className = '' }) {
  const [status, setStatus] = useState('loading')
  const [useExternal, setUseExternal] = useState(false)

  const r2Url = item.r2_path ? `/images/${item.r2_path}` : null
  const externalUrl = item.imagem_url
  const primarySrc = useExternal ? externalUrl : r2Url
  const src = primarySrc || externalUrl

  if (!src || status === 'error') {
    return (
      <div className={`bg-[#E8E3DC] flex items-center justify-center ${className}`}>
        <div className="text-center text-[#8B7355]">
          <span className="text-2xl">⚖️</span>
          <p className="font-serif text-xs italic mt-1">{item.titulo}</p>
        </div>
      </div>
    )
  }

  return (
    <img
      src={src}
      alt={`${item.titulo} — ${item.pais_nome || ''} — ${item.data_estimada || ''}`}
      className={className}
      loading="lazy"
      onLoad={() => setStatus('loaded')}
      onError={() => {
        if (!useExternal && externalUrl) {
          setUseExternal(true)
          setStatus('loading')
        } else {
          setStatus('error')
        }
      }}
    />
  )
}
