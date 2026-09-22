import { useState } from 'react'
import { BookOpen, ChevronRight } from 'lucide-react'

const CATEGORIES = [
  {
    id: 'conceitos-tese',
    title: '🔍 Conceitos da Tese',
    description: 'Termos originais desenvolvidos na pesquisa',
    color: 'border-l-[#6B1E3A]'
  },
  {
    id: 'warburg',
    title: '🎨 Escola de Warburg',
    description: 'Terminologia da tradição histórico-artística',
    color: 'border-l-[#2D4A3E]'
  },
  {
    id: 'regimes',
    title: '⚖️ Regimes Iconocráticos',
    description: 'Classificação das alegorias jurídicas',
    color: 'border-l-[#C9A961]'
  },
  {
    id: 'metodologia',
    title: '📊 Metodologia',
    description: 'Procedimentos analíticos e codificação',
    color: 'border-l-[#8B7355]'
  }
]

const GLOSSARY = [
  {
    term: 'ICONOCRACIA',
    category: 'conceitos-tese',
    definition: 'Governo pelas imagens — poder das alegorias visuais na construção do Estado e do direito',
    context: 'Conceito central da tese, cunhado a partir da análise do corpus'
  },
  {
    term: 'Endurecimento',
    category: 'conceitos-tese',
    definition: 'Processo de codificação que transforma imagens em categorias fechadas, apagando nuances históricas',
    context: 'Antônimo de "abertura" ou "plasticidade" simbólica'
  },
  {
    term: 'Contrato Sexual Visual',
    category: 'conceitos-tese',
    definition: 'Estrutura de poder reproduzida nas alegorias jurídicas que subordinam mulheres à autoridade masculina',
    context: 'Conceito original, desenvolvido a partir de Carole Pateman (1988)'
  },
  {
    term: 'Feminilidade de Estado',
    category: 'conceitos-tese',
    definition: 'Performance de gênero encenada por alegorias femininas que representam instituições estatais',
    context: 'Alegorias femininas não são mulheres reais, mas personificações de poder'
  },
  {
    term: 'Contrato Racial Visual',
    category: 'conceitos-tese',
    definition: 'Estrutura de exclusão racial naturalizada através da iconografia jurídica ocidental',
    context: 'Conceito original, desenvolvido a partir de Charles Mills (1997)'
  },
  {
    term: 'Purificação Clássica',
    category: 'conceitos-tese',
    definition: 'Operação simbólica que remove traços materiais, históricos e afetivos das alegorias',
    context: 'Manifesta-se nos 10 indicadores de endurecimento'
  },
  {
    term: 'Pathosformel',
    category: 'warburg',
    definition: 'Fórmula patética — imagem que condensa afetos e memórias culturais através do tempo',
    context: 'Aby Warburg (1866–1929), estudioso da tradição clássica no Renascimento'
  },
  {
    term: 'Zwischenraum',
    category: 'warburg',
    definition: 'Espaço intermediário — zona de trânsito entre significados culturais e históricos',
    context: 'Imagens operam em Zwischenräume, não em categorias fechadas'
  },
  {
    term: 'Nachleben',
    category: 'warburg',
    definition: 'Vida póstuma — sobrevivência e transformação de imagens através das épocas',
    context: 'Alegorias jurídicas são Nachleben de figuras clássicas'
  },
  {
    term: 'Mnemosyne Atlas',
    category: 'warburg',
    definition: 'Projeto inacabado de Warburg: organização visual de Pathosformeln em painéis comparativos',
    context: 'Inspiração metodológica para o Atlas Warburg do companion'
  },
  {
    term: 'Fundacional',
    category: 'regimes',
    definition: 'Regime iconocrático de alegorias que legitimam a fundação do Estado e suas instituições',
    context: 'Exemplo: Marianne (França), República (Brasil), Columbia (EUA)'
  },
  {
    term: 'Normativo',
    category: 'regimes',
    definition: 'Regime iconocrático de alegorias que representam ordem jurídica e aplicação da lei',
    context: 'Exemplo: Iustitia cega, Themis, Minerva em tribunais'
  },
  {
    term: 'Militar',
    category: 'regimes',
    definition: 'Regime iconocrático de alegorias em contextos bélicos, coloniais ou de expansão',
    context: 'Exemplo: Britannia em moedas coloniais, Marianne em cartazes de guerra'
  },
  {
    term: 'Contra-Alegoria',
    category: 'regimes',
    definition: 'Regime iconocrático de imagens que contestam ou subvertem alegorias dominantes',
    context: 'Exemplo: grafites feministas, paródias contemporâneas'
  },
  {
    term: 'Indicadores de Endurecimento',
    category: 'metodologia',
    definition: '10 códigos de análise que medem o grau de "purificação clássica" nas alegorias',
    context: '1. Desincorporação, 2. Rigidez Postural, 3. Dessexualização, 4. Uniformização Facial, 5. Heraldização, 6. Enquadramento Arquitetônico, 7. Apagamento Narrativo, 8. Monocromatização, 9. Serialidade, 10. Inscrição Estatal'
  },
  {
    term: 'Codificação Iconográfica',
    category: 'metodologia',
    definition: 'Procedimento de análise que atribui valores (0-3) aos indicadores de endurecimento',
    context: 'Score total 0-30 permite graduação comparativa entre alegorias'
  },
  {
    term: 'Corpus',
    category: 'metodologia',
    definition: 'Conjunto de 265 imagens catalogadas de alegorias jurídicas (França, Brasil, UK, Alemanha, Itália, EUA, Áustria, Portugal, Suíça, Grécia, Japão, Espanha)',
    context: 'Compilado entre 2025-2026, período de 1800-1950'
  }
]

export default function Glossario() {
  const [activeCategory, setActiveCategory] = useState('conceitos-tese')
  const [expanded, setExpanded] = useState(null)

  const filtered = GLOSSARY.filter(g => g.category === activeCategory)
  const activeCat = CATEGORIES.find(c => c.id === activeCategory)

  return (
    <div className="anim-fade-in px-8 pt-8 pb-16 max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-10">
        <div className="flex items-center gap-3 mb-3">
          <BookOpen size={24} className="text-[#6B1E3A]" />
          <h1 className="font-serif text-4xl text-[#6B1E3A] tracking-wide">Glossário</h1>
        </div>
        <p className="text-sm text-[#8B7355] leading-relaxed max-w-2xl">
          Termos-chave da tese ICONOCRACIA e da tradição metodológica de Aby Warburg.
          Organizado em categorias para facilitar navegação e referência rápida.
        </p>
      </div>

      <div className="grid grid-cols-[250px_1fr] gap-8">
        {/* Sidebar */}
        <aside className="space-y-1 sticky top-[120px] self-start">
          {CATEGORIES.map(cat => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`w-full text-left px-4 py-3 rounded-lg transition-all duration-300 border-l-4 ${
                activeCategory === cat.id
                  ? 'vintage-card ' + cat.color + ' shadow-md'
                  : 'hover:bg-[rgba(201,169,97,0.1)] border-l-transparent'
              }`}
            >
              <div className="font-serif text-lg text-[#6B1E3A] mb-0.5">{cat.title}</div>
              <div className="text-[11px] text-[#8B7355]">{cat.description}</div>
            </button>
          ))}
        </aside>

        {/* Content */}
        <div className="space-y-4">
          {filtered.map((item, i) => (
            <div
              key={item.term}
              className="anim-card vintage-card rounded-lg p-5 transition-all duration-300 cursor-pointer hover:shadow-lg hover:-translate-y-0.5"
              onClick={() => setExpanded(expanded === i ? null : i)}
              style={{ animationDelay: `${i * 0.03}s` }}
            >
              <div className="flex items-start justify-between">
                <h3 className="font-serif text-xl text-[#6B1E3A] mb-1">{item.term}</h3>
                <ChevronRight
                  size={16}
                  className={`text-[#8B7355] transition-transform duration-300 ${expanded === i ? 'rotate-90' : ''}`}
                />
              </div>
              <p className="text-sm text-[#3D2817] leading-relaxed">{item.definition}</p>
              {expanded === i && item.context && (
                <div className="mt-3 pt-3 border-t border-[rgba(139,115,85,0.2)] anim-fade-in">
                  <p className="text-xs text-[#8B7355] leading-relaxed italic">{item.context}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
