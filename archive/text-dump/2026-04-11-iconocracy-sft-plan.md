# Plano v1 — SFT ICONOCRACY com TRL

**Data**: 2026-04-11  
**Objetivo**: construir um assistente especializado da tese ICONOCRACY por meio de SFT (Supervised Fine-Tuning) com QLoRA sobre um modelo instruct multilíngue forte em português.  
**Método**: TRL `SFTTrainer` + Transformers + PEFT/QLoRA.  
**Modelo-base recomendado**: `Qwen/Qwen2.5-7B-Instruct`.

---

## 1. Decisão estratégica

O alvo não é um chatbot jurídico genérico nem um classificador visual puro. O alvo é um **assistente de pesquisa e redação da tese**, capaz de:

1. respeitar a terminologia mandatória do projeto;
2. operar dentro da cadeia de rastreabilidade do corpus;
3. transformar registros estruturados do corpus em análise acadêmica útil;
4. redigir em português com voz jurídico-histórica consistente;
5. apoiar capítulos, metodologia, interpretação e síntese sem romper os guardrails da tese.

Por isso, o treino v1 será **SFT de comportamento e transformação textual**, não RLHF e não PPO/GRPO.

---

## 2. Escolha do modelo e do ambiente

### Modelo
- **Primário**: `Qwen/Qwen2.5-7B-Instruct`
- **Piloto mais barato**: `Qwen/Qwen2.5-3B-Instruct`

### Método
- **QLoRA**, não full fine-tuning
- sequência-alvo: **2048 tokens**
- treino de 2–3 épocas para o v1

### Ambiente
- **Não usar o Mac local** para o treino principal
- **Preferir GPU CUDA remota**, idealmente:
  - **A100 40GB** para a corrida principal
  - L4 apenas para pilotos ou redução de batch/expectativa

### Saída
- checkpoints/adapters fora do repositório Git
- diretório recomendado de artefatos:
  - `~/Models/iconocracy-qwen25-7b-sft-lora`

No repositório, guardar apenas:
- scripts
- configs
- manifestos
- dataset preparado em JSONL, se o tamanho for razoável

---

## 3. Fontes canônicas para o dataset v1

### Fontes principais já identificadas
1. `AGENT_CONFIG_ICONOCRACIA.md`
2. `AGENTS.md`
3. `docs/superpowers/specs/2026-04-11-thesis-chapter-plan.md`
4. `docs/superpowers/specs/2026-04-11-project-update-plan.md`
5. `data/processed/records.jsonl`
6. `data/processed/purification.jsonl`

### Papel de cada fonte
- `AGENT_CONFIG_ICONOCRACIA.md` / `AGENTS.md`
  - regras editoriais
  - terminologia obrigatória
  - cadeia de rastreabilidade
  - identidade epistemológica do projeto
- `thesis-chapter-plan.md`
  - estrutura da tese
  - dependências entre capítulos
  - riscos, lacunas e prioridades
- `project-update-plan.md`
  - versão prudente do projeto
  - formulação estratégica para banca, hipótese, metodologia e sumário
- `records.jsonl`
  - matéria-prima de transformação corpus → análise
- `purification.jsonl`
  - matéria-prima de interpretação dos indicadores e do endurecimento

---

## 4. Mistura recomendada do dataset

### Distribuição sugerida
- **40%** transformação de corpus em análise
- **25%** explicação metodológica e teórica
- **20%** planejamento/redação de capítulos e seções
- **15%** guardrails, terminologia e estilo

### Tarefas-alvo
1. **Corpus → nota analítica**
   - entrada: registro bruto ou quase bruto do `records.jsonl`
   - saída: parágrafo analítico com vocabulário da tese

2. **Indicadores → interpretação**
   - entrada: linha de `purification.jsonl`
   - saída: leitura interpretativa do nível de purificação/endurecimento

3. **Planejamento de tese**
   - entrada: pergunta sobre capítulo, dependência, risco ou ordem de redação
   - saída: resposta ancorada nos planos já aprovados

4. **Terminologia / guardrails**
   - entrada: solicitação ambígua, termo errado ou fluxo inadequado
   - saída: correção alinhada às regras do projeto

---

## 5. O que entra e o que não entra

### Entra
- documentos estáveis já aprovados ou maduros
- exemplos de transformação estruturada → prosa acadêmica
- exemplos que reforcem a voz jurídico-histórica do projeto
- exemplos que preservem a terminologia mandatória

### Não entra
- notas provisórias confusas
- material que contradiga a fase atual do projeto
- saídas que traduzam `endurecimento`
- respostas que tratem a IA como substituta da leitura do usuário
- outputs que quebrem a cadeia `fonte → Drive → scripts → records.jsonl → corpus/tese`

---

## 6. Objetivo operacional do v1

O v1 deve ficar bom em:
- explicar o projeto
- sugerir redação acadêmica aderente à tese
- transformar registros do corpus em análise inicial útil
- interpretar indicadores de purificação
- respeitar rigor terminológico e metodológico

O v1 **não precisa** ainda ficar bom em:
- preferência fina entre estilos de escrita concorrentes
- RLHF com julgamentos humanos comparativos
- raciocínio visual direto sobre imagens sem camada multimodal
- classificação estatística nova

---

## 7. Sequência de execução recomendada

### Fase A — Dataset v1
1. gerar JSONL em formato de chat
2. inspecionar 50 exemplos manualmente
3. remover exemplos redundantes ou com prosa ruim
4. congelar `train`/`validation`

### Fase B — Piloto rápido
1. rodar piloto em `Qwen2.5-3B-Instruct`
2. testar terminologia, voz e transformação corpus → análise
3. corrigir dataset se o modelo estiver:
   - genérico demais
   - prolixo demais
   - estilisticamente frouxo
   - conceitualmente impreciso

### Fase C — Corrida principal
1. subir para `Qwen2.5-7B-Instruct`
2. QLoRA com 2–3 épocas
3. avaliar qualitativamente em prompts reais da tese

---

## 8. Hiperparâmetros iniciais recomendados

- learning rate: `2e-5`
- epochs: `2`
- per-device batch: `2`
- gradient accumulation: `8`
- max sequence length: `2048`
- lora rank: `16`
- lora alpha: `32`
- lora dropout: `0.05`
- bf16: `true` quando suportado
- gradient checkpointing: `true`
- eval split: `5%` a `10%`

---

## 9. Critérios de sucesso

O treino v1 será considerado bem-sucedido se o modelo:

1. usar corretamente:
   - Contrato Sexual Visual
   - Feminilidade de Estado
   - endurecimento
   - Pathosformel / Zwischenraum / Nachleben
2. não deslizar para antropologia/sociologia genérica quando a tarefa exige voz jurídico-histórica;
3. produzir notas analíticas úteis a partir de `records.jsonl`;
4. interpretar `purification.jsonl` de modo consistente com os regimes iconocráticos;
5. responder perguntas de planejamento da tese com aderência aos documentos aprovados.

---

## 10. Arquivos criados para esta fase

- `docs/superpowers/specs/2026-04-11-iconocracy-sft-plan.md`
- `docs/superpowers/specs/2026-04-11-iconocracy-sft-dataset-spec.md`
- `tools/scripts/build_iconocracy_sft_dataset.py`
- `tools/scripts/train_iconocracy_sft.py`
- `tools/configs/training/iconocracy_qwen25_7b_qlora.json`

---

## 11. Próximo passo recomendado

Rodar o builder do dataset em modo piloto, inspecionar amostras e só então iniciar o treino remoto.
