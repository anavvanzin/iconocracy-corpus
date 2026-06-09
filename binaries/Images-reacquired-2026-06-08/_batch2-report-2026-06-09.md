# Re-aquisição Batch 2 — Relatório — 2026-06-09

**Escopo:** 33 itens restantes do set de 51 com HTML/PDF salvo como `.jpg` (docs/decisions/nao-imagens-store-2026-05-30.json), excluindo os 18 do Batch 1 (Numista + Rijksmuseum).

---

## Resumo

| Resultado | Count |
|-----------|-------|
| OK (imagem válida adquirida) | 0/33 |
| Institutional Access | 4/33 |
| NEEDS_MANUAL | 1/33 |
| HTTP 403 (cloud IP block) | 27/33 |
| Bot-protected | 1/33 |

**Causa raiz:** O container cloud desta sessão tem IP bloqueado por Cloudflare e CDNs de museus/arquivos em TODOS os 33 domínios. Requisições diretas (`urllib`) retornam HTTP 403. O Exa conseguiu buscar HTML de alguns sites (BildIndex, IMS, Brasiliana, LucasCranach, DHM, BNE, museos.gub.uy) mas não retorna conteúdo binário. Este é um bloqueio de IP de provedor cloud — a aquisição precisa ser feita do laptop da Ana.

---

## Tabela por item

| ID | Domain | Status | Notes |
|----|--------|--------|-------|
| BE-001 | collections.heritage.brussels | HTTP_403 | Cloudflare block; page not fetched via Exa |
| BE-002 | be-monumen.be | HTTP_403 | HTTP 403 from container |
| BR-005 | archive.nyu.edu | HTTP_403 | TIFF: `/bitstream/2451/61396/2/Rj12-03.tiff`; thumbnail JPG: `/retrieve/124973/Rj12-03.tiff.jpg` |
| BR-006 | brasiliana.museus.gov.br | HTTP_403 | Alegoria da República, Chambelland 1922; Brasiliana code `f9686ffb4f947dbec319d3d63abefccf` |
| BR-007 | memoria.bn.br | HTTP_403 | PDF per702390; download manual + pdftoppm -f 60 -l 60 -jpeg -r 200 |
| BR-009 | acervos.ims.com.br | HTTP_403 | "A Justiça" Ceschiatti, id 010ACDF27248.jpg; requer liberação IMS |
| BR-010 | eliseuvisconti.com.br | HTTP_403 | D702 O Progresso c.1910 pastel; Fundação Biblioteca Nacional RJ |
| DE-001 | bildindex.de | HTTP_403 | que20183316 — Exa timeout; tente diretamente do laptop |
| DE-002 | bildindex.de | HTTP_403 | obj08148970 — Justitia 1239-40 Capua; Datengeber: `http://foto.biblhertz.it/obj08148970` |
| DE-003 | bildindex.de | HTTP_403 | obj30110594 — Göttin der Gerechtigkeit, Bernhard Rode; Deutsche Fotothek FD 253 077 |
| DE-004 | bildindex.de | HTTP_403 | obj20553978 — Justitia an der Rathausuhr 1589 Esslingen; Bildarchiv Foto Marburg mi05228a07 |
| DE-005 | bildindex.de | HTTP_403 | obj20672587 — Personifikation Gerechtigkeit 1660/1780 Lüneburg; Bildarchiv mi07014d04 |
| DE-006 | bildindex.de | HTTP_403 | obj08158050 — Allegorie Justitia, Raimondi; Datengeber: `http://foto.biblhertz.it/obj08158050` |
| DE-007 | bildindex.de | HTTP_403 | obj08108743 — Exa timeout; tente do laptop |
| DE-008 | bildindex.de | HTTP_403 | obj20608421 — Justitia um 1558 Hameln; Deutsche Fotothek FD 351 316 |
| DE-009 | bildindex.de | HTTP_403 | obj20459153 — Exa timeout; tente do laptop |
| DE-010 | bildindex.de | HTTP_403 | obj20677105 — Jus Civile, Wenzinger 1752, Sankt Peter; Bildarchiv mi08920i01 |
| DE-011 | bildindex.de | HTTP_403 | obj30143134 — Kamin mit Justitia um 1610 Leipzig; Deutsche Fotothek FD 115 733 |
| DE-012 | lucascranach.org | HTTP_403 | Justice 1537 PRIVATE_NONE-P457; colecção privada; CDA page load OK via Exa |
| DE-013 | dhm.de | HTTP_403 | Kaulbach Germania 1914, DHM Inv. 1988/82; solicitar via fotoservice@dhm.de |
| DE-GERM-1900 | en.wikipedia.org | HTTP_403 | **Wikimedia Commons:** `File:DR_1900_56_Germania_Reichspost.jpg` (570×670, domínio público) |
| DE-GERM-BELG-1914 | colnect.com | BOT_PROTECTED | Anubis Proof-of-Work; necessita browser real |
| ES-001 | bdh.bne.es | HTTP_403 | BNE item 76944; IIIF: `bdh.bne.es/bnesearch/rest/imagen/iiif/manifest?id=76944` |
| ES-002 | hemerotecadigital.bne.es | HTTP_403 | Hemeroteca card sid=3971781; jornal 1637; IIIF disponível via BNE API |
| PT-001 | bndigital.bnportugal.gov.pt | INSTITUTIONAL_ACCESS | Item 17148 Justiça popular; **"acessível apenas na rede interna da BNP"** |
| PT-002 | bndigital.bnportugal.gov.pt | INSTITUTIONAL_ACCESS | Item 39213 Alegoria à História; institucional BNP only |
| PT-003 | bndigital.bnportugal.gov.pt | INSTITUTIONAL_ACCESS | Item 37491 Alegoria à Morte; institucional BNP only |
| PT-004 | bndigital.bnportugal.gov.pt | INSTITUTIONAL_ACCESS | Item 37507 Alegoria ao Tempo; institucional BNP only |
| UK-001 | britishmuseum.org | HTTP_403 | BM P_1870-0625-185; Exa timeout; tentar BM IIIF: `https://www.britishmuseum.org/collection/image/...` |
| UK-002 | britishmuseum.org | HTTP_403 | BM P_1862-0712-304; Exa timeout |
| UK-003 | britishmuseum.org | HTTP_403 | BM P_1862-0712-305; Exa timeout |
| UK-004 | speel.me.uk | HTTP_403 | Site estático; Exa timeout; tente `curl` do laptop |
| UY-001 | museos.gub.uy | NEEDS_MANUAL | Página de biografia de Blanes — sem imagem específica da obra na URL; identificar imagem correta manualmente |

---

## Diagnóstico por grupo

### BildIndex.de (11 itens: DE-001–DE-011)

O BildIndex funciona como agregador de imagens de partner portals com direitos reservados. Os 11 itens pertencem a três instituições:

- **Bibliotheca Hertziana (Roma):** DE-002 e DE-006 → `http://foto.biblhertz.it/obj08148970` e `obj08158050`
- **Deutsche Fotothek:** DE-003, DE-008, DE-011 → buscar via `https://www.deutschefotothek.de/`
- **Bildarchiv Foto Marburg:** DE-004, DE-005, DE-010 e mais → `https://www.fotomarburg.de/`
- DE-001, DE-007, DE-009 → Exa timeout; tentar do laptop diretamente

**Estratégia laptop:** abrir cada URL no browser, esperar o viewer carregar, clicar "Download" ou fazer screenshot do viewer.

### BNPortugal (4 itens: PT-001–PT-004)

Acesso restrito à rede interna da BNP. Opções:
1. Solicitar cópia via `bndigital@bnportugal.pt` com referência aos persistent IDs (`purl.pt/22074` para PT-001)
2. Visitar a BNP presencialmente (Lisboa)
3. Verificar se as obras têm acesso via IIIF público: `https://iiif.bnportugal.gov.pt/iiif/...`

### British Museum (3 itens: UK-001–UK-003)

BM tem IIIF. URLs padrão:
- `https://iiif.thebritishmuseum.org/image/api/v3/iiif/P_1870-0625-185/full/full/0/default.jpg` (adaptar por item)
- Alternativamente: `https://media.britishmuseum.org/media/Repository/...` — verificar do laptop

### Wikimedia Commons (1 item: DE-GERM-1900)

**Download imediato do laptop:**
```
wget "https://upload.wikimedia.org/wikipedia/commons/a/a7/DR_1900_56_Germania_Reichspost.jpg" -O DE-GERM-1900.jpg
```
(ou qualquer outro arquivo da série: `DR_1900_55_Germania_Reichspost.jpg` para o 5Pf)

### Misc (BR-005, BR-006, BR-007, BR-009, BR-010, DE-012, DE-013, DE-GERM-BELG-1914, ES-001, ES-002, UK-004, UY-001)

Ver tabela acima para URLs e estratégias por item.

---

## Próximos passos recomendados (para Ana, do laptop)

1. **DE-GERM-1900**: Download imediato do Wikimedia (link acima) — 1 min
2. **BildIndex 11 itens**: Abrir no browser, screenshots ou download via viewer — ~30 min
3. **BM 3 itens**: Testar IIIF URLs diretamente do laptop
4. **PT 4 itens**: Solicitar à BNP via email com persistent IDs
5. **BR-007**: `wget http://memoria.bn.br/pdf/702390/per702390_1827_00060.pdf && pdftoppm -f 60 -l 60 -jpeg -r 200 BR-007.pdf BR-007`
6. **Demais**: Ver notas na tabela por item

---

*Relatório gerado em 2026-06-09 por sessão remota Claude Code (reacquire-images-batch2). O script de aquisição está em `tools/scripts/_batch2_acquire.py` para reutilização do laptop.*
