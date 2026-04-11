# Próximo passo operacional — piloto 3B

A recomendação atual é executar o piloto barato antes da corrida 7B.

## Script único

Arquivo:
- `tools/scripts/run_iconocracy_3b_pilot.sh`

Ele faz, em sequência:
1. treino do adapter LoRA 3B
2. avaliação do modelo base
3. avaliação do modelo fine-tunado

## Uso em GPU remota

```bash
cd iconocracy-corpus
bash tools/scripts/run_iconocracy_3b_pilot.sh
```

## Saídas esperadas

- adapter: `~/Models/iconocracy-qwen25-3b-sft-pilot-lora`
- eval base: `data/training/eval_base_qwen3b.jsonl`
- eval fine-tuned: `data/training/eval_ft_qwen3b.jsonl`

## O que observar depois

Comparar base vs fine-tuned em:
- terminologia (`ENDURECIMENTO`, `Feminilidade de Estado`)
- método (`QUAN→QUAL→síntese`, IconoCode)
- planejamento da tese
- transformação de registros do corpus em notas analíticas

Se o ganho for claro, a próxima decisão racional é subir para o 7B.
