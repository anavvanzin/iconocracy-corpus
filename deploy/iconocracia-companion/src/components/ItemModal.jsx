import { useEffect, useCallback } from 'react'
import { X, Copy, ChevronLeft, ChevronRight } from 'lucide-react'
import ImageLoader from './ImageLoader'

const FLAGS = { FR:'🇫🇷', BR:'🇧🇷', UK:'🇬🇧', DE:'🇩🇪', IT:'🇮🇹', US:'🇺🇸', AT:'🇦🇹', PT:'🇵🇹', CH:'🇨🇭', GR:'🇬🇷', JP:'🇯🇵', ES:'🇪🇸' }

export default function ItemModal({ item, onClose, onPrev, onNext, allItems }) {
  const handleKey = useCallback(e => {
    if (e.key === 'Escape') onClose()
    if (e.key === 'ArrowLeft') onPrev?.()
    if (e.key === 'ArrowRight') onNext?.()
  }, [onClose, onPrev, onNext])

  useEffect(() => {
    document.addEventListener('keydown', handleKey)
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', handleKey)
      document.body.style.overflow = ''
    }
  }, [handleKey])

  if (!item) return null

  const related = (allItems || [])
    .filter(i => i.id !== item.id && (i.regime === item.regime || i.pais === item.pais))
    .slice(0, 4)

  const copyCitation = () => {
    if (item.citacao_abnt) navigator.clipboard.writeText(item.citacao_abnt)
  }

  return (
    <div
      className="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm flex justify-end"
      onClick={e => e.target === e.currentTarget && onClose()}
      role="dialog"
      aria-modal="true"
      aria-label={`Detalhe: ${item.titulo}`}
    >
      <div className="w-[420px] max-w-[90vw] h-screen overflow-y-auto bg-[#FAF7F2] border-l border-[rgba(139,115,85,0.25)] p-8 relative"
           style={{ animation: 'slideInRight 0.3s cubic-bezier(0.22, 1, 0.36, 1)' }}>
        <button onClick={onClose} className="absolute top-4 right-4 text-[#8B7355] hover:text-[#3D2817] text-xl" aria-label="Fechar">
          <X size={20} />
        </button>
        <div className="absolute top-4 left-4 flex gap-1">
          {onPrev && <button onClick={onPrev} className="p-1 text-[#8B7355] hover:text-[#3D2817]"><ChevronLeft size={18} /></button>}
          {onNext && <button onClick={onNext} className="p-1 text-[#8B7355] hover:text-[#3D2817]"><ChevronRight size={18} /></button>}
        </div>

        <div className="w-full rounded border border-[rgba(139,115,85,0.25)] mb-5 overflow-hidden">
          <ImageLoader item={item} className="w-full h-[280px] object-cover" />
        </div>

        <h2 className="font-serif text-[22px] text-[#6B1E3A] mb-1">{item.titulo}</h2>
        <p className="text-[13px] text-[#8B7355] mb-5">
          {[item.autor, item.acervo, item.data_estimada].filter(Boolean).join(' · ')}
        </p>

        <Field label="País">{FLAGS[item.pais] || '🏳️'} {item.pais_nome}</Field>
        {item.suporte && <Field label="Suporte">{item.suporte}</Field>}
        {item.regime && <Field label="Regime iconocrático">{item.regime}</Field>}
        {item.motivo && <Field label="Motivo alegórico">{item.motivo}</Field>}

        {item.endurecimento && (
          <Field label="Endurecimento detectado">
            <span className={item.endurecimento.detectado ? 'text-[#6B1E3A]' : 'text-green-700'}>
              {item.endurecimento.detectado ? 'Sim' : 'Não'}
              {item.endurecimento.detalhe && ` — ${item.endurecimento.detalhe}`}
            </span>
          </Field>
        )}

        {item.citacao_abnt && (
          <div className="mt-4">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[10px] font-semibold tracking-widest uppercase text-[#8B7355]">Citação (ABNT)</span>
              <button onClick={copyCitation} className="text-[#8B7355] hover:text-[#6B1E3A]" title="Copiar citação">
                <Copy size={12} />
              </button>
            </div>
            <p className="font-mono text-[11px] leading-relaxed text-[#3D2817]">{item.citacao_abnt}</p>
          </div>
        )}

        {item.tags?.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-4">
            {item.tags.map(t => (
              <span key={t} className="text-[10px] px-2 py-0.5 rounded bg-[#E8E3DC] text-[#3D2817]">{t}</span>
            ))}
          </div>
        )}

        {related.length > 0 && (
          <div className="mt-6 pt-4 border-t border-[rgba(139,115,85,0.25)]">
            <h3 className="font-serif text-base text-[#6B1E3A] mb-3">Conexões</h3>
            {related.map(r => (
              <div key={r.id} className="flex items-center gap-2 py-1.5 text-[13px] text-[#3D2817] hover:text-[#6B1E3A] cursor-pointer">
                <div className="w-8 h-8 bg-[#E8E3DC] rounded border border-[rgba(139,115,85,0.25)] flex-shrink-0 overflow-hidden">
                  <ImageLoader item={r} className="w-full h-full object-cover" />
                </div>
                <span>{r.titulo} — {r.pais_nome}, {r.data_estimada}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function Field({ label, children }) {
  return (
    <div className="mb-3.5">
      <span className="block text-[10px] font-semibold tracking-widest uppercase text-[#8B7355] mb-0.5">{label}</span>
      <span className="text-sm text-[#3D2817]">{children}</span>
    </div>
  )
}
