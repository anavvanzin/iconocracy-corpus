# Entrega ABNT — O contrato visual

## Escopo e proveniência

- Manuscrito de partida: `../O contrato visual.md` (220 linhas; preservado).
- Estrutura complementar: `../../../../tese/pesquisa/genealogia-alegoria-feminina.md` e `../genealogia-alegoria-feminina.json` (quatro teses; 903 linhas; fontes preservadas).
- Cópia de segurança do manuscrito: `original/O contrato visual.md`.
- Artigo integral de entrega: `O contrato visual — integral ABNT.md`, `.docx` e `.pdf`.
- As seções 5 e 6 foram redigidas a partir das teses 03 e 04 e dos quadros genealógicos da estrutura; o texto adicional está isolado em `expansao-integral.md` para revisão autoral.

## Normalização e composição

- Referências e citações em sistema autor-data, orientadas pelas ABNT NBR 6023:2025 e NBR 10520:2023.
- Página A4; Times New Roman 12; margens superior/esquerda de 3 cm e inferior/direita de 2 cm; corpo com espaçamento 1,5; referências com espaçamento simples e separação entre entradas.
- As três citações parentéticas com Resnik e Curtis foram normalizadas para `Resnik; Curtis`.
- A citação direta de Warner com `p. xx` foi convertida em paráfrase; nenhuma página foi inventada.
- Outras expressões sem página foram convertidas em paráfrase quando a operação era segura. A atribuição a Haraway sem obra identificada foi retirada da cópia de entrega. O manuscrito original permanece íntegro.
- A referência a Mondzain (2002), presente na estrutura, foi incorporada para sustentar a nova seção. São 24 entradas bibliográficas na cópia integral.
- O registro `changes.jsonl` discrimina as intervenções automáticas. `build_abnt.py` e `reference-abnt.docx` permitem reproduzir a compilação.

## Pendências de fonte antes de submissão

1. Confirmar os dados completos de Hayaert (2023), sobretudo título do periódico, local, volume/fascículo e páginas. A entrada foi preservada conforme o manuscrito; sua existência e exatidão não foram certificadas nesta normalização.
2. Conferir a localização do Decreto n. 4/1889 na *Coleção das Leis do Brasil* (volume e páginas, se aplicáveis).
3. Rever no exemplar consultado as atribuições conceituais a Behrmann (`axioma do espelho`) e Gonzalez (`racismo por denegação`), além dos enunciados factuais sobre objetos e datas. Aspas conceituais não substituem a localização de uma citação literal.
4. Conferir a nova seção autoralmente, em especial a tipologia dos regimes e a extensão de conceitos da tese ao artigo. Os exemplos comparativos nela mencionados não foram convertidos em afirmações empíricas validadas sobre cada objeto.
5. Esta entrega normaliza e compõe o artigo; não equivale à verificação integral de referências, imagens e afirmações exigida pelo estágio de integridade do `academic-pipeline`.

## Verificações da entrega

- PDF gerado pelo Pandoc/XeLaTeX em A4 e inspecionado visualmente.
- DOCX aberto por `python-docx` para verificar dimensões, margens e estilos.
- Texto extraído do PDF conferido quanto à presença das novas seções e das referências.
- `git diff --check` e compilação de `build_abnt.py` executados.
- Não houve commit, push nem alteração do manuscrito de partida.
