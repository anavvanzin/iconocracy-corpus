# Piloto barato — ICONOCRACY SFT

## Config escolhido
- `tools/configs/training/iconocracy_qwen25_3b_qlora_pilot.json`

## Objetivo
Validar rapidamente se o dataset v1.1 move o modelo na direção certa antes de investir numa corrida 7B maior.

## Razão da escolha
- `Qwen/Qwen2.5-3B-Instruct` ainda é forte o bastante para mostrar mudança de comportamento
- custa menos tempo e VRAM do que 7B
- é suficiente para medir ganho em:
  - terminologia
  - método
  - planejamento
  - transformação de registros do corpus

## Parâmetros
- 1 época
- contexto 1536
- batch maior que o 7B
- QLoRA 4-bit

## Expectativa
O piloto não precisa produzir o modelo final. Ele precisa responder à pergunta certa:

> O dataset v1.1 realmente especializa o modelo para ICONOCRACY de forma perceptível?

Se a resposta for sim, então o 7B passa a ser investimento racional.
