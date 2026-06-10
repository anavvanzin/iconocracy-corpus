export default function Counter({ count, label = 'itens no corpus' }) {
  if (count === null || count === undefined) return null
  return (
    <div className="text-xs text-[#8B7355] tracking-wide">
      <strong className="text-[#6B1E3A] font-semibold text-sm">{count}</strong>
      <span className="ml-1.5">{label}</span>
    </div>
  )
}
