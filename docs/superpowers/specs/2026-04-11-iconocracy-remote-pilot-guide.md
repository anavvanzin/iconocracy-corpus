# Guia de execução remota — piloto SFT ICONOCRACY

## Objetivo

Executar um piloto barato e rápido antes da corrida principal de 7B.

Recomendação de piloto:
- modelo: `Qwen/Qwen2.5-3B-Instruct`
- config: `tools/configs/training/iconocracy_qwen25_3b_qlora_pilot.json`
- dataset: `data/training/iconocracy_sft_v1_1_train.jsonl` + `data/training/iconocracy_sft_v1_1_val.jsonl`

---

## 1. Opção mais simples: GPU remota por SSH

### Requisitos mínimos razoáveis
- GPU com 24 GB VRAM ou mais
- CUDA funcional
- Python 3.10+ ou 3.11+

### Sequência
```bash
git clone https://github.com/anavvanzin/iconocracy-corpus.git
cd iconocracy-corpus
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install transformers datasets peft accelerate trl bitsandbytes sentencepiece
python tools/scripts/train_iconocracy_sft.py --config tools/configs/training/iconocracy_qwen25_3b_qlora_pilot.json
```

### Avaliação pós-treino
```bash
python tools/scripts/run_iconocracy_eval.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --prompts data/training/iconocracy_eval_prompts_v1_1.jsonl \
  --output data/training/eval_base_qwen3b.jsonl

python tools/scripts/run_iconocracy_eval.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --adapter ~/Models/iconocracy-qwen25-3b-sft-pilot-lora \
  --prompts data/training/iconocracy_eval_prompts_v1_1.jsonl \
  --output data/training/eval_ft_qwen3b.jsonl
```

---

## 2. Modal

Use Modal se quiser execução reproduzível sem manter VM manualmente, mas com mais setup inicial.

### Estratégia sugerida
- criar image com Python + CUDA + libs de treino
- montar ou clonar o repositório no job
- persistir artefatos do LoRA em volume remoto

### Comando de treino a embutir no job Modal
```bash
python tools/scripts/train_iconocracy_sft.py --config tools/configs/training/iconocracy_qwen25_3b_qlora_pilot.json
```

### Quando usar Modal
- quando quiser repetir vários pilotos com o mesmo ambiente
- quando preferir script declarativo a sessão SSH manual

### Quando evitar Modal
- quando quiser apenas um teste rápido hoje
- quando ainda estiver ajustando dataset e config com frequência

---

## 3. RunPod / Vast.ai

Essas opções são boas para piloto barato se você já estiver confortável com GPU spot/rentada.

### Fluxo recomendado
1. subir instância CUDA com 24 GB+
2. clonar repo
3. criar venv
4. instalar dependências
5. rodar treino com o config piloto
6. baixar adapter final e logs

### Vantagem
- geralmente mais barato que manter box tradicional

### Desvantagem
- mais fricção operacional do que um SSH box já pronto
- persistência e volumes exigem mais atenção

---

## 4. Ordem de execução recomendada

### Passo 1 — Piloto barato
```bash
python tools/scripts/train_iconocracy_sft.py --config tools/configs/training/iconocracy_qwen25_3b_qlora_pilot.json
```

### Passo 2 — Avaliação base vs fine-tuned
```bash
python tools/scripts/run_iconocracy_eval.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --prompts data/training/iconocracy_eval_prompts_v1_1.jsonl \
  --output data/training/eval_base_qwen3b.jsonl

python tools/scripts/run_iconocracy_eval.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --adapter ~/Models/iconocracy-qwen25-3b-sft-pilot-lora \
  --prompts data/training/iconocracy_eval_prompts_v1_1.jsonl \
  --output data/training/eval_ft_qwen3b.jsonl
```

### Passo 3 — Só então subir para 7B
Se o piloto mostrar ganho claro em:
- terminologia
- método
- planejamento
- corpus-to-analysis

então vale rodar:
```bash
python tools/scripts/train_iconocracy_sft.py --config tools/configs/training/iconocracy_qwen25_7b_qlora.json
```

---

## 5. Critério prático de escolha do provider

### Use SSH box se:
- você quer o caminho mais direto
- já tem acesso a uma GPU remota
- quer depurar rápido

### Use Modal se:
- quer reprodutibilidade e jobs declarativos
- aceita gastar um pouco mais de setup agora para repetir depois

### Use RunPod/Vast se:
- quer piloto barato por hora
- não se importa em lidar com alguma fricção operacional

---

## 6. Recomendação objetiva

Para o momento atual do projeto, o melhor caminho é:
1. **piloto 3B em uma GPU remota simples por SSH**
2. **avaliar base vs adapter com o eval set**
3. **só então decidir o 7B principal**
