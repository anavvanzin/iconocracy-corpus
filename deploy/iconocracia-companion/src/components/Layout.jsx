import Nav from './Nav'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 relative">
        {children}
      </main>
      <footer className="px-8 py-5 border-t border-[rgba(107,30,58,0.2)] bg-gradient-to-r from-[#E8DCC4] via-[#EDE2C5] to-[#E8DCC4]">
        <p className="text-[10px] text-[#6B1E3A] tracking-[2px] uppercase text-center font-medium">
          PPGD/UFSC · Ana Vanzin · Doutorado 2026
        </p>
        <p className="text-[9px] text-[#8B7355] tracking-wider uppercase text-center mt-1">
          Orientação: Georges Martyn (UGent) & Arno Dal Ri Júnior (UFSC)
        </p>
      </footer>
    </div>
  )
}
