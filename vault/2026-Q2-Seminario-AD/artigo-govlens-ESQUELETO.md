# ESQUELETO — Artigo GovLens / DueProcess.AI

## Título provisório
"Do Poder-Dever ao Dever-Poder: o Conselho de Contestação Algorítmica como Arquitetura de Devido Processo Legal na Administração Pública 4.0"

## Autores
Ana Vitória Vanzin & Vinícius Oliveira (PPGD/UFSC)

## Estrutura IMRAD adaptada (artigo de direito + protótipo)

### Resumo (~250 palavras)
- Problema: Estado como maior controlador de dados e usuário de algoritmos, com incentivo estrutural a subaplicar normas contra o cidadão
- Lacuna: não há no Brasil plataforma que integre explicabilidade + mapa de dados + geração de peças jurídicas + painel de viés + simulação de exclusão
- Método: design science research + protótipo funcional (FastAPI + React + LLMs via OpenRouter)
- Resultado: Conselho de Contestação Algorítmica (4 personas mapeadas 1:1 nos artigos do IJDL)
- Caso-âncora: INSS (negativa automática de aposentadoria rural)
- Conclusão: o protótipo encarna a dogmática em software; a Administração Pública 4.0 só é legítima quando subordinada a mecanismos efetivos de contestação

### Palavras-chave
Administração Pública digital; contestabilidade algorítmica; devido processo legal; explicabilidade; LGPD; inteligência artificial no setor público

### 1. Introdução — O Estado como Regulador ⇄ Regulado
- Tese autoral: "Do Poder-Dever ao Dever-Poder"
- O mesmo aparato que edita LAI/LGPD/ANPD/CNJ é o maior controlador de dados
- Incentivo estrutural a subaplicar a norma contra o cidadão
- Pergunta de partida: como materializar o contraditório algorítmico prévio (CF, art. 5º, LV) quando a decisão é automatizada?
- Apresentação do GovLens/DueProcess.AI como resposta prototípica
- Delimitação: protótipo acadêmico/conceitual, não produto comercial

### 2. Diagnóstico: a lacuna de contestabilidade no Brasil
- Fala.BR: canal de comunicação, não análise jurídica
- "Conteste Aqui" (CadÚnico): específico, sem explicabilidade
- Dataprev (Auxílio Emergencial): regras rígidas, sem estratégia jurídica
- DPU: requer intervenção de defensor, não é autosserviço
- Gov.br app (LGPD art. 20): canal, não ferramenta de análise
- Tabela comparativa de funcionalidades (o que existe × o que falta)
- Dados TIC Domicílios 2024: 22% conectividade significativa, 3% classes DE
- Veredicto: ninguém integra explicabilidade + mapa de dados + geração de pedidos + painel de viés + simulação de exclusão num único fluxo

### 3. Marco teórico: quatro artigos, quatro eixos
- 3.1 Contraditório algorítmico prévio (Tavares, Bitencourt & Cristóvam, IJDL 2020)
  - Explicabilidade como condição de validade da decisão automatizada
  - Art. 5º, LV da CF + Lei 9.784/1999 (motivação)
- 3.2 Autodeterminação informativa e proteção de dados (Salgado & Saito, IJDL 2020; Sarlet & Molinaro, IJDL 2020)
  - Multifuncionalidade do direito fundamental à proteção de dados
  - LGPD art. 20: revisão de decisões automatizadas
  - Big data na saúde como cenário-limite
- 3.3 Governo aberto e dados orientados (Cristóvam & Hahn, IJDL 2020)
  - Infraestrutura nacional de dados abertos
  - Lei 14.129/2021 (Lei do Governo Digital)
  - Transparência × inteligibilidade
- 3.4 Tese do Regulador ⇄ Regulado
  - Síntese dos quatro eixos
  - Estado como maior usuário de algoritmos e simultaneamente regulador

### 4. O protótipo: GovLens / DueProcess.AI
- 4.1 Conceito: plataforma de contestabilidade
  - Não é ouvidoria nem produto comercial
  - Fluxo: cidadão entra com decisão automatizada → plataforma traduz, audita e arma contestação
- 4.2 Arquitetura técnica
  - Backend: FastAPI (Python), porta 8001
  - Frontend: React/Vite, porta 5173
  - LLMs: OpenRouter (Claude 3.5 Sonnet, GPT-4o, Gemini 1.5, Llama 3.1)
  - Armazenamento: JSON local
  - Código aberto: github.com/anavvanzin/algoritmo-em-disputa
- 4.3 Fluxo unificado (7 telas)
  - Tela 0: Camada propedêutica ("Você sabe que foi uma máquina?")
  - Tela 1: Consulta/Upload
  - Tela 2: Motivação ou caixa-preta?
  - Tela 3: Mapa de dados
  - Tela 4: Conselho de Contestação (o motor)
  - Tela 5: Estratégia jurídica (minutas LAI/LGPD/recurso)
  - Tela 6: Tensão democrática (eficiência × direitos × controle × inclusão)

### 5. O Conselho de Contestação Algorítmica: o motor do protótipo
- 5.1 Desenho: 4 personas, 3 fases
  - Fase 1: pareceres paralelos (cada persona emiti parecer independente)
  - Fase 2: avaliação cruzada anônima (personas leem e criticam os pareceres umas das outras)
  - Fase 3: Relator sintetiza parecer fundamentado
- 5.2 Mapeamento persona → artigo → eixo jurídico (TABELA CENTRAL)
  - Defensoria Pública ↔ Tavares, Bitencourt & Cristóvam ↔ contraditório algorítmico prévio (art. 5º, LV)
  - Cientista de Dados ↔ transversal ↔ XAI, viés de proxy, transparência
  - Administrador Público ↔ Cristóvam & Hahn ↔ governo aberto, governança, Lei 14.129
  - Cidadão/Direitos Digitais ↔ Salgado & Saito + Sarlet & Molinaro ↔ autodeterminação informativa, LGPD, exclusão digital
  - Relator ↔ síntese final ↔ integração dos quatro eixos
- 5.3 Implementação
  - config.py: definição das personas (linhas 20-47)
  - council.py: fluxo de 3 fases (linhas 26-171)
  - main.py: API POST /api/conversations/{id}/message

### 6. Caso-âncora: INSS — negativa automática de aposentadoria rural
- 6.1 O caso
  - Indeferimento automático de aposentadoria rural
  - Sem contraditório prévio
  - Em desacordo com a IN 128/2022
  - Caso central da tabela do seminário
- 6.2 Precedente internacional: SyRI (Haia, 2020)
  - Sistema de Risco Indicativo de Fraude
  - Corte de Haia: violação do art. 8 CEDH (vida privada)
  - Dever de explicabilidade e transparência algorítmica
- 6.3 Demonstração do protótipo com o caso INSS
  - O que o Conselho produziu: parecer com ~7.000 caracteres
  - As 4 perspectivas + a síntese do Relator
  - Minutas geradas: pedido LAI, requerimento LGPD art. 20, recurso administrativo

### 7. Contribuições propedêuticas (camada autoral)
- 7.1 Literacia algorítmica antes da contestação
  - O contraditório pressupõe que o cidadão saiba que houve decisão algorítmica
  - Distinção: transparência ≠ inteligibilidade
  - Materialização: Tela 0 ("Você sabe que foi uma máquina?")
- 7.2 Notícia humana para vulneráveis
  - Tese normativa: comunicação de decisão adversa a vulnerável deve ser feita por humano
  - Dignidade do administrado está em como ele é avisado
  - Materialização: flag de notícia humana no fluxo

### 8. Discussão
- 8.1 O que o protótipo demonstra que a dogmática isoladamente não demonstra
  - A encarnação em software força precisão: cada persona deve emitir parecer fundamentado, não genérico
  - A avaliação cruzada revela contradições entre eixos
  - O Relator como síntese mostra que os quatro artigos são complementares, não concorrentes
- 8.2 Limites do protótipo
  - Protótipo conceitual, não validado empiricamente com usuários reais
  - Modelos LLM podem alucinar fundamentação jurídica
  - Custos de API (modelos pagos via OpenRouter)
  - Não substitui advogado, defensor ou controlador
- 8.3 Limites da abordagem
  - Foco no âmbito federal (INSS); generalização para municípios requer adaptação
  - LGPD art. 20 §1º: regulamentação ainda em curso pela ANPD
  - Dependência de infraestrutura digital (exclusão digital como limite material)

### 9. Conclusão
- Síntese: o protótipo encarna a tese do Regulador ⇄ Regulado em software
- Cada persona do Conselho é uma voz da bibliografia do seminário
- O caso INSS condensa os quatro eixos
- Originalidade: integração crítica num único fluxo (Fala.BR e "Conteste Aqui" não fazem)
- Frase final: "A Administração Pública 4.0 só é legítima quando a eficiência do uso de dados e algoritmos está subordinada a mecanismos efetivos de contestação, correção de erros e inclusão digital — assegurando o contraditório e a ampla defesa."

### Referências (ABNT NBR 6023:2025)
- IJDL articles (4 centrais)
- Legislation: CF/88, Lei 9.784/99, Lei 12.527/11, Lei 13.709/18, Lei 14.129/21
- TIC Domicílios 2024
- SyRI / Rechtbank Den Haag (2020)
- Araújo, Zullo & Torres (2020)
- Fernández González (2016)
- Friedrich & Philippi (2020)
- Literatura adicional sobre explicabilidade, XAI, contestabilidade

### Figuras sugeridas
- Fig. 1: Diagrama Regulador ⇄ Regulado (tese central)
- Fig. 2: Arquitetura do GovLens/DueProcess.AI (7 telas)
- Fig. 3: Fluxo do Conselho de Contestação (3 fases)
- Fig. 4: Mapeamento persona → artigo → eixo jurídico
- Fig. 5: Tela do protótipo com caso INSS (screenshot)
- Fig. 6: Tela de estratégia jurídica (minutas geradas)
