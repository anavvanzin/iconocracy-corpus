---
title: Arquitetura Atlas e Tese — MOC
aliases:
  - Mapa do Site e Separação Atlas-Tese
  - Do Mármore à Margem
  - Muta Imago
  - Lex Hysteria
type: kg/moc
tags:
  - kg
  - projeto/iconocracia
  - arquitetura
  - tese
related:
  - "[[Iconocracia — Mapa Central]]"
  - "[[Conceitos — MOC]]"
  - "[[Hierarquia de Dados — MOC]]"
  - "[[Manuscrito — MOC]]"
status: ativo
created: 2026-11-02
updated: 2026-11-02
---

# Arquitetura: O Atlas Aberto (`ICONOCRACIA`) vs. A Tese Focada (`1822–1922`)

> [!important] Princípio de Desacoplamento Ontológico
> O site **`iconocracia.com`** e a **tese de doutorado** cumprem funções epistemológicas distintas e complementares:
> 1. **`ICONOCRACIA` (`iconocracia.com`)** é o **Atlas de Iconologia Jurídica e Laboratório de Experimentação Visual** (transnacional, `1800–2000`, 17+ países, expansão crítica do *Iconclass* via **Contra-Arquivo**, painéis warburguianos de coexistência e experimentos interativos como a *FUNDIÇÃO*).
> 2. **A Tese de Doutorado (Brasil, `1822–1922`)** é uma **trilha de pesquisa focada (*Strand*)** dentro do Atlas — com títulos provisórios em avaliação autoral:
>    - ***Do Mármore à Margem*** *(proposta provisória)*
>    - ***Muta Imago*** *(proposta provisória)*
>    - ***Lex Hysteria*** *(proposta provisória)*

---

## 1. A Tríade da *Matriz* (*Hystera ➔ Matriz de Aço ➔ Matriz Digital*)

No tratado hipocrático *Doenças das Mulheres* (*Gynaikeia*), a patologia feminina decorre do **Deslocamento**: o útero (*hystera*) desprende-se e vagueia pelo corpo, causando sufocação e desordem até ser pesado e ancorado no lugar.

Aplicado à iconografia jurídica oitocentista e novecentista, esse mito médico revela o mecanismo exato de **Do Mármore à Margem** / **Muta Imago** / **Lex Hysteria**:
1. **Hystera (ὑστέρα) ➔ Tutela Civil à Margem:** O direito positivo (Ordenações Filipinas, Decreto nº 181/1890, Código Civil de 1916, art. 6º II e art. 242) diagnosticou as mulheres vivas como sujeitos instáveis que exigiam tutela civil às margens da cidadania.
2. **Matriz Numismática e Monumental (Casa da Moeda):** A arte de Estado «curou» essa indisciplina percebida fundindo o corpo feminino na imobilidade do mármore, do bronze e da moeda. A tradução direta latina e portuguesa do grego *hystera* é ***matrix* (*matriz*)** — exatamente o termo técnico para o cunho de aço gravado na Seção de Gravura da Casa da Moeda do Brasil (Carneiro, Girardet, Villares) para estampar a efígie estatal nas moedas, enquanto, em sentido warburguiano (*Bilderwanderung*), essas imagens alegóricas recusavam-se a ficar paradas, migrando através de oceanos, regimes, moedas e tribunais.
3. **Matriz Digital (O Contra-Arquivo):** A grade estrutural da base de dados que confronta o catálogo administrativo passivo (*Iconclass* no Eixo Esquerdo) com a operação jurídico-política (*Reivindicações / Claims* e *Conceitos* no Eixo Direito).

---

## 2. Mapa das 5 Superfícies de `iconocracia.com`

| Rota | Superfície | Escopo | Entidades do Modelo |
| :--- | :--- | :--- | :--- |
| `/` | **O Atlas (Campo Constelacional)** | Transnacional (`1800–2000`) | `Constellation` (previews), Dossiês de Coexistência, entrada para as Trilhas |
| `/acervo` e `/acervo/[id]` | **O Contra-Arquivo (Catálogo Dual-Axis)** | 337+ objetos documentados + Lente Raio-X | **Eixo Esquerdo:** `Object`, `Image`, `Source` (ABNT NBR 6023:2025), `Iconclass` (`31AA`, `44G0`, `48C24`, `44B`)<br>**Eixo Direito:** `Claim` (aprovadas), `Concept`, Coexistência Temporal |
| `/constelacoes` e `/constelacoes/[slug]` | **Painéis Warburguianos** | Montagens comparativas (*Columbia*, *Marianne*, *Brasil*, *Hystera/Matriz*) | `Constellation` (*Elo visual* · *Elo histórico documentado* · *Leitura proposta*) |
| `/conceitos` e `/experimentos` (`/jogo`) | **Léxico Crítico & Laboratório Visual** | Vocabulário proprietário + *FUNDIÇÃO* (`/jogo`) | `Concept` (`31AA::CSV`, `44G0::FE`, `48C24::PC`, `44B::CRV`, `48C24::MM`), `Experiment` |
| `/trilhas/brasil-1822-1922` (`/tese`) | **Trilha Doutoral: Brasil (1822–1922)** | Recorte estrito da tese (53 itens BR + matrizes de transferência + Casa da Moeda `CMB-AUD-01..07`) | `Strand`, 4 Capítulos Híbridos, Protocolo Norma-Imagem |
