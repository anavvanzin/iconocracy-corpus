# Conselho de Modelos — Veredicto sobre o Piloto de Recodificação

**Data:** 24 de julho de 2026
**Pergunta:** o piloto (15 registros) está bom o suficiente para escalar aos 144 restantes? Pode ser melhorado?
**Revisores independentes:** Gemini 3 Pro · GPT-5.5 · Claude Opus 4.8 (cada um avaliou o mesmo dossiê às cegas, sem ver as respostas dos outros)

---

## Veredicto unânime: NÃO ESCALAR AINDA

Os três modelos convergiram — sem contato entre si — para o mesmo diagnóstico:
o método é sólido na **execução visual** (ver a imagem, verificar URLs, corrigir
catalogação), mas frágil na **construção da métrica**. Escalar agora contaminaria
a distribuição de ENDURECIMENTO dos 328 registros.

## Placar consolidado (0–10)

| Critério | Gemini | GPT-5.5 | Opus | Média |
|----------|:------:|:-------:|:----:|:-----:|
| (a) Validade de construto | 4 | 6 | 4 | **4,7** |
| (b) Consistência dos indicadores | 5 | 5 | 3 | **4,3** |
| (c) Lógica de atribuição de regime | 3 | 5 | 3 | **3,7** |
| (d) Tratamento honesto de dados ausentes | 2 | 6 | 5 | **4,3** |
| (e) Reprodutibilidade em escala | 3 | 4 | 3 | **3,3** |

O ponto mais fraco, unânime, é **reprodutibilidade** (3,3) — sem codebook ancorado
e sem dupla codificação, os 144 restantes não replicariam.

---

## Os três defeitos que todos apontaram

### 1. Regime é atribuído por intenção/contexto, não por forma visual
- `US-BANNER-1861`: Columbia dinâmica e viva (score 1,3) foi rotulada **MILITAR**
  só porque a litografia é dedicada a um general em campanha.
- `DE-GERM-1900`: selo definitivo civil rotulado **NORMATIVO** mas com score 3,0
  por militarismo "latente" (coroa, couraça sugerida).
- Consequência: a atribuição de regime fica **infalsificável** e não reproduzível —
  o maior risco de confiabilidade entre codificadores.

### 2. O problema da ausência (o mais grave)
- `FR-ASSIGNAT-1792` **não tem corpo feminino** (águia + fasces + barrete), mas
  recebeu `desincorporacao=4`, `dessexualizacao=4` e **score 3,0** — o mais alto
  do piloto.
- Os três revisores classificam isso como **erro de categoria**: pontuar um corpo
  ausente como "endurecimento máximo" fabrica um pico de ENDURECIMENTO a partir do
  nada, desloca a média para cima e **falsamente sustentaria a tese**.
- **Correção unânime:** ausência estrutural do corpo → ENDURECIMENTO = **NULO/NA**,
  contada como categoria separada (`corpo_ausente` / ANICÔNICO), nunca como ponto
  numérico no contínuo 0–4.

### 3. Inflação da métrica pelo suporte (apontado por Opus e GPT)
- `serialidade`, `monocromatizacao` e `inscricao_estatal` são quase automaticamente
  3–4 para qualquer moeda ou selo circulante — medem o **suporte**, não o corpo.
- Isso enviesa toda a distribuição para "endurecimento alto" independentemente da
  figura. Considerar normalizar esses indicadores dentro de cada tipo de suporte.

### Defeito adicional: confiança não controla o score
- Imagens diluídas/baixa resolução (ex.: `BR-041` score 1,3; `03a9622f` score 2,7)
  ainda emitem os 10 indicadores com o mesmo peso das leituras de alta confiança.

---

## Melhorias exigidas antes de escalar (consenso)

1. **Codebook ancorado** — um exemplar visual escrito por indicador por nível
   (0,1,2,3,4). Ex. para `rigidez_postural`: 0=correndo/voando · 2=de pé parada ·
   4=busto congelado. Pontuar SÓ o que está representado.
2. **Separar regime de score** — atribuir regime por árvore de decisão visual;
   proibir dedicatória/intenção/uso histórico como evidência. Opcional: piso
   numérico (score < 1,5 não pode ser MILITAR).
3. **Regra formal de ausência** — gate binário "há corpo alegórico feminino?";
   se não, pular os 10 indicadores, ENDURECIMENTO = NULO, categoria própria.
4. **Gating por confiança** — imagem abaixo do limiar de resolução/verificação
   entra só como flag, não emite score quantitativo.
5. **Dupla codificação + confiabilidade entre avaliadores** — 20–30% dos itens
   codificados às cegas por dois codificadores; reportar Kappa/Krippendorff α
   (alvo ≥ 0,67–0,70) ANTES de escalar.
6. **Campos separados** no schema — score visual · regime · suporte · contexto
   político · tipo de ausência/recusa. Exigir nota de evidência para todo score ≥3
   e para toda divergência regime↔score.
