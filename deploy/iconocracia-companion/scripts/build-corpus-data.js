#!/usr/bin/env node
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.resolve(__dirname, '..', '..', '..')
const RECORDS = path.join(ROOT, 'data', 'processed', 'records.jsonl')
const OUTPUT = path.join(__dirname, '..', 'src', 'data', 'corpus.json')

fs.mkdirSync(path.dirname(OUTPUT), { recursive: true })

if (!fs.existsSync(RECORDS)) {
  console.error('❌ records.jsonl not found at:', RECORDS)
  process.exit(1)
}

const lines = fs.readFileSync(RECORDS, 'utf-8').trim().split('\n')
const records = lines.map(l => JSON.parse(l))

const COUNTRY_NAMES = {
  FR: 'França', BR: 'Brasil', UK: 'Reino Unido', DE: 'Alemanha',
  IT: 'Itália', US: 'EUA', AT: 'Áustria', PT: 'Portugal',
  CH: 'Suíça', GR: 'Grécia', JP: 'Japão', ES: 'Espanha',
  NL: 'Holanda', BE: 'Bélgica', RU: 'Rússia', AR: 'Argentina',
}

const items = records.map((r, idx) => ({
  id: r.id || `IC-${String(idx + 1).padStart(3, '0')}`,
  titulo: r.titulo || r.title || 'Sem título',
  autor: r.autor || r.author || null,
  data_estimada: r.data_estimada || r.date || null,
  pais: r.pais || r.country || null,
  pais_nome: COUNTRY_NAMES[r.pais] || r.pais_nome || r.pais || null,
  suporte: r.suporte || r.support || null,
  regime: r.regime || r.regime_iconografico || null,
  motivo: r.motivo || r.motivo_alegorico || r.description || null,
  tags: Array.isArray(r.tags) ? r.tags : [],
  endurecimento: r.endurecimento || null,
  imagem_url: r.imagem_url || r.url || r.image_url || null,
  r2_path: r.r2_path || null,
  citacao_abnt: r.citacao_abnt || r.citacao || null,
  acervo: r.acervo || r.collection || null,
  confianca: r.confianca || null,
  related: Array.isArray(r.related) ? r.related : [],
}))

const por_pais = {}, por_regime = {}, por_suporte = {}, por_decada = {}
items.forEach(item => {
  if (item.pais) por_pais[item.pais] = (por_pais[item.pais] || 0) + 1
  if (item.regime) por_regime[item.regime] = (por_regime[item.regime] || 0) + 1
  if (item.suporte) por_suporte[item.suporte] = (por_suporte[item.suporte] || 0) + 1
  if (item.data_estimada) {
    const decada = Math.floor(parseInt(item.data_estimada) / 10) * 10
    if (!isNaN(decada)) por_decada[decada] = (por_decada[decada] || 0) + 1
  }
})

const corpus = {
  meta: { total: items.length, generated: new Date().toISOString(), source: 'data/processed/records.jsonl' },
  items,
  stats: { por_pais, por_regime, por_suporte, por_decada },
}

fs.writeFileSync(OUTPUT, JSON.stringify(corpus, null, 2))
console.log(`✅ corpus.json: ${items.length} items → ${OUTPUT}`)
