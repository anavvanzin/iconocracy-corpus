#!/usr/bin/env python3
"""
gallery_ingest.py — Integrate gallery/ research results into corpus-data.json.

Performs three operations:
1. Enriches existing duplicate entries with new metadata from gallery
2. Appends new items from gallery research
3. Generates SCOUT notes in vault/candidatos/

Usage:
    python tools/scripts/gallery_ingest.py                # dry run
    python tools/scripts/gallery_ingest.py --apply         # apply changes
    python tools/scripts/gallery_ingest.py --apply --notes # apply + generate SCOUT notes
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
VAULT_DIR = REPO_ROOT / "vault" / "candidatos"

TODAY = "2026-04-03"
SOURCE = "gallery-perplexity-2026-04-03"

# ─── ENRICHMENTS for existing duplicates ───────────────────────────────────

ENRICHMENTS = {
    "FR-005": {  # Rops
        "thumbnail_url": "https://gallica.bnf.fr/ark:/12148/btv1b531842166.highres",
        "_merge_description": "Eau-forte, pointe sèche et inscriptions à la plume ; 16,9 × 13 cm. BnF cote: RESERVE CC-82 (B, 2)-FOL. Refs: Rouir 649, Ramiro 178, Exteens 330, Mascha 479.",
    },
    "FR-008": {  # Steinlen "République appelle"
        "thumbnail_url": "https://gallica.bnf.fr/ark:/12148/btv1b10510623s.highres",
        "_merge_description": "Lithographie en noir ; 55,9 × 69 cm (grand format). BnF cote: FT 5-DC-385 (G, 1). Ref: Christophe 26a. Collector: Atherton Curtis (1863–1943).",
    },
    "FR-010": {  # Veber "Hochet"
        "thumbnail_url": "https://gallica.bnf.fr/ark:/12148/btv1b8577647w.highres",
        "_merge_description": "Lithographie en couleurs ; 43 × 26 cm et 36,5 × 31 cm (2 states). Variant ARK: btv1b8577647w. Satirical composition on Separation of Church and State debates.",
    },
    "FR-001": {  # Chifflart "Justice, Vengeance, Vérité"
        "_merge_description": "Dimensions: 23,9 × 31,7 cm. Ancien possesseur: Musée du Luxembourg (Paris, 1818–1937). Ref: Sueur G-10.",
    },
    "FR-002": {  # Chifflart "Triomphe"
        "_merge_description": "Ref: Sueur G-8. Companion print to FR-001.",
    },
    "FR-003": {  # Chifflart "L'envoyé"
        "_merge_description": "Early Chifflart work (1859). Dimensions: 27,4 × 19,3 cm.",
    },
    "FR-009": {  # Agence Rol busts
        "_merge_description": "Series of 4 press photographs: ark btv1b6952880n, btv1b69528812, btv1b6952882g, btv1b69528790. Documents official Marianne busts during WWI.",
    },
    "FR-018": {  # Ernouf letterhead
        "_merge_description": "Military letterhead with female allegories of Republic, Force, Liberty triumphing over Austria, Britain, Papacy, and French monarchy.",
    },
    "FR-022": {  # Veber "Notre-Dame des colonies"
        "_merge_description": "Anti-colonialist satirical print. Marianne recast as 'Notre-Dame des colonies' with colonized peoples (Chinese, Africans) and armed colonizers.",
    },
    "FR-029": {  # Emprunt national 1920
        "_merge_description": "Post-WWI national loan poster (Société centrale des banques de province). Related series: btv1b10051217v, btv1b100506817, btv1b100512528, btv1b10051241d, btv1b10051230j, btv1b10051244r, btv1b10051246n, btv1b100512310, btv1b100505003.",
    },
    "BR-005": {  # Villares
        "_merge_description": "Also catalogued on Senado Tainacan as 'Dama da República': https://tainacan.senado.leg.br/personalidades/dama-da-republica/. NYU Archive: https://archive.nyu.edu/handle/2451/61396.",
    },
    "BR-006": {  # Chambelland
        "_merge_description": "Also on Brasiliana Museus: https://brasiliana.museus.gov.br/acervos/alegoria-da-republica/. MHN acervo museológico n. 6232. Dimensions: 202 × 152 cm, óleo sobre tela.",
    },
    "BR-009": {  # Ceschiatti exterior
        "_merge_description": "Wikimedia Commons: 62 images at https://commons.wikimedia.org/wiki/Category:Justi%C3%A7a_(Alfredo_Ceschiatti). Agência Senado Flickr: https://www.flickr.com/photos/agenciasenado/46826464635. Vandalized Jan 8, 2023; attacked again Nov 13, 2024.",
    },
}


def make_item(id, title, date, year, period, creator, institution, source_archive,
              country, medium, motif, description, url, thumbnail_url="",
              medium_norm=None, country_pt=None, period_norm=None,
              support=None, tags=None, citation_abnt=None, citation_chicago=None,
              in_scope=True, scope_note=None, regime=None):
    """Create a corpus-data.json item with all required fields."""
    return {
        "id": id,
        "title": title,
        "date": date,
        "period": period,
        "creator": creator,
        "institution": institution,
        "source_archive": source_archive,
        "country": country,
        "medium": medium,
        "motif": motif or [],
        "description": description,
        "url": url,
        "thumbnail_url": thumbnail_url,
        "rights": "Public domain" if country == "France" else "Public access",
        "citation_abnt": citation_abnt,
        "citation_chicago": citation_chicago,
        "tags": tags or ["gallery-batch", f"#verificar"],
        "year": year,
        "medium_norm": medium_norm,
        "country_pt": country_pt or ("Brasil" if country == "Brazil" else "França" if country == "France" else None),
        "period_norm": period_norm,
        "motif_str": ", ".join(motif) if motif else None,
        "tags_str": ", ".join(tags) if tags else None,
        "regime": regime,
        "endurecimento_score": None,
        "indicadores": None,
        "coded_by": None,
        "coded_at": None,
        "support": support,
        "in_scope": in_scope,
        "scope_note": scope_note,
        "panofsky": None,
    }


# ─── NEW BRAZILIAN ITEMS ──────────────────────────────────────────────────

NEW_BR = [
    make_item(
        id="BR-011",
        title="Glória à Pátria! Homenagem da Revista Illustrada (Angelo Agostini)",
        date="1889-11-16", year=1889,
        period="Early Republic (1889–1930)",
        creator="Angelo Agostini (atrib.)",
        institution="Biblioteca Nacional",
        source_archive="Hemeroteca Digital Brasileira",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Alegoria feminina", "Marianne brasileira", "Barrete frígio"],
        description="First personified representation of the Republic as a female figure in the Revista Illustrada, published the day after the Proclamation. Central female figure in Greco-Roman dress with Phrygian cap, sword, shield, and Brazilian flag. Alongside Marshal Deodoro da Fonseca on horseback. Considered the inaugural 'Brazilian Marianne' in the illustrated press.",
        url="http://memoria.bn.gov.br/DocReader/332747b/4260",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["Marianne brasileira", "Proclamação", "Agostini", "Revista Illustrada", "barrete frígio"],
        citation_abnt="AGOSTINI, Angelo (atrib.). Glória à Pátria! Homenagem da Revista Illustrada. Revista Illustrada, Rio de Janeiro, ano 14, n. 569, p. 10, 16 nov. 1889. Disponível em: http://memoria.bn.gov.br/DocReader/332747b/4260.",
        citation_chicago="Agostini, Angelo (attrib.). \"Glória à Pátria! Homenagem da Revista Illustrada.\" Revista Illustrada, year 14, no. 569, p. 10, November 16, 1889. Hemeroteca Digital. http://memoria.bn.gov.br/DocReader/332747b/4260.",
    ),
    make_item(
        id="BR-012",
        title="Alegoria da República — Festa do 13 de Maio (Abolição)",
        date="1890-05", year=1890,
        period="Early Republic (1889–1930)",
        creator="Unknown (Revista Illustrada)",
        institution="Biblioteca Nacional",
        source_archive="Hemeroteca Digital Brasileira",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Abolição", "Alegoria feminina", "Barrete frígio", "Carro alegórico"],
        description="Illustration of the commemorative celebration of the Lei Áurea anniversary organized by the Confederação Abolicionista. Three female allegories on a parade float: two conductors seated in front, one prominent figure on top with red Phrygian cap holding the republican celestial sphere. Documents the Republic-Abolition association.",
        url="http://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=332747&pesq=alegoria",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["Abolição", "Lei Áurea", "carro alegórico", "Revista Illustrada", "Confederação Abolicionista"],
        citation_abnt="ALEGORIA da República — Festa do 13 de Maio. Revista Illustrada, Rio de Janeiro, n. 590, maio 1890. Disponível em: http://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=332747.",
    ),
    make_item(
        id="BR-013",
        title="Alegoria da República — 3.º Aniversário da Lei Áurea",
        date="1891-05", year=1891,
        period="Early Republic (1889–1930)",
        creator="Unknown (Revista Illustrada)",
        institution="Biblioteca Nacional",
        source_archive="Hemeroteca Digital Brasileira",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Abolição", "Alegoria feminina", "Barrete frígio", "Canhão"],
        description="Female figure of the Republic with Phrygian cap and Brazilian flag on a staff wrapped around her arm. A discharged cannon pointing at 'Lei 13 de maio' inscription. First time the female allegory appears isolated (without the indigenous figure) as the periodical's republican symbol in this context.",
        url="http://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=332747&pesq=republica",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["Abolição", "Lei Áurea", "Revista Illustrada", "barrete frígio", "bandeira"],
        citation_abnt="ALEGORIA da República — 3.º Aniversário da Lei Áurea. Revista Illustrada, Rio de Janeiro, n. 621, maio 1891. Disponível em: http://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=332747.",
    ),
    make_item(
        id="BR-014",
        title="Alegoria da República — 13 de Maio de 1893",
        date="1893-05", year=1893,
        period="Early Republic (1889–1930)",
        creator="Unknown (Revista Illustrada)",
        institution="Biblioteca Nacional",
        source_archive="Hemeroteca Digital Brasileira",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Abolição", "Alegoria feminina", "Grilhões rompidos"],
        description="Elegant female figure (Brazilian Marianne) with broken shackles in her hands. Under her feet, a globe inscribed 'Brazil 13 de maio de 1888'. Greco-Roman dress. The allegory assumes responsibility for abolition, erasing Princess Isabel's and the monarchy's protagonism in the new republican context.",
        url="http://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=332747b",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["Abolição", "grilhões", "Marianne brasileira", "Revista Illustrada"],
        citation_abnt="ALEGORIA da República — 13 de Maio de 1893. Revista Illustrada, Rio de Janeiro, capa, maio 1893. Disponível em: http://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=332747b.",
    ),
    make_item(
        id="BR-015",
        title="Alegoria da República Brasileira (Revista Illustrada, Wikimedia)",
        date="1876–1898", year=1889,
        period="Early Republic (1889–1930)",
        creator="Angelo Agostini (atrib.)",
        institution="Biblioteca Nacional",
        source_archive="Wikimedia Commons",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Alegoria feminina"],
        description="Female figure in Greco-Roman dress representing the Brazilian Republic. Digitized from Revista Illustrada, public domain. Original from UFSC.",
        url="https://commons.wikimedia.org/wiki/File:Republica_no_brasil.jpg",
        thumbnail_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Republica_no_brasil.jpg/455px-Republica_no_brasil.jpg",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["Marianne brasileira", "Agostini", "Revista Illustrada", "Wikimedia"],
        citation_abnt="AGOSTINI, Angelo (atrib.). [Alegoria da República Brasileira]. [1876–1898]. 1 litografia. Revista Illustrada. Disponível em: https://commons.wikimedia.org/wiki/File:Republica_no_brasil.jpg.",
    ),
    make_item(
        id="BR-016",
        title="Alegoria da República (Manoel Lopes Rodrigues)",
        date="1896", year=1896,
        period="Early Republic (1889–1930)",
        creator="Manoel Lopes Rodrigues (1861–1917)",
        institution="Museu de Arte da Bahia",
        source_archive="dezenovevinte.net",
        country="Brazil", medium="Oil on canvas",
        motif=["República", "Alegoria feminina", "Barrete frígio", "Marianne"],
        description="Oil on canvas (230 × 120 cm). Female figure in Greco-Roman dress. White Phrygian cap (usually red) placed on her head by the hand of Providence emerging from a palm tree. Red cloak (allusion to France). Severe expression, non-youthful figure — contrasts with conventional Marianne representations. Commissioned under Prudente de Morais, executed in Paris. Considered an 'exceptional work' and 'poetic license' within the allegorical repertoire.",
        url="http://www.dezenovevinte.net/obras/mlr_rapj.htm",
        medium_norm="Pintura", period_norm="República/Império (BR)",
        support="óleo sobre tela",
        tags=["Lopes Rodrigues", "Museu de Arte da Bahia", "barrete frígio", "Marianne brasileira", "positivismo"],
        citation_abnt="LOPES RODRIGUES, Manoel. Alegoria da República. 1896. 1 pintura, óleo sobre tela, 230 × 120 cm. Museu de Arte da Bahia, Salvador. Análise em: http://www.dezenovevinte.net/obras/mlr_rapj.htm.",
        citation_chicago="Lopes Rodrigues, Manoel. Alegoria da República. 1896. Oil on canvas, 230 × 120 cm. Museu de Arte da Bahia, Salvador. http://www.dezenovevinte.net/obras/mlr_rapj.htm.",
    ),
    make_item(
        id="BR-017",
        title="O Ano de 1896 — Marianne brasileira vs. francesa (Angelo Agostini, Don Quixote)",
        date="1896", year=1896,
        period="Early Republic (1889–1930)",
        creator="Angelo Agostini",
        institution="Senado Federal — BDSF",
        source_archive="Biblioteca Digital do Senado Federal",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Marianne brasileira", "Marianne francesa", "Satira"],
        description="Cover illustration of Don Quixote. Brazilian Republic as a sad woman with Phrygian cap and Brazilian flag, pulled away by statesmen. In the background, vigorous French Marianne leading horses in the opposite direction. Don Quixote and Sancho Panza observe inertly. Visual contrast between the French republican ideal and the frustrated Brazilian republic ('Maria').",
        url="https://www2.senado.leg.br/bdsf/handle/id/507627",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["Don Quixote", "Agostini", "Marianne", "sátira", "contraste BR-FR"],
        citation_abnt="AGOSTINI, Angelo. O Ano de 1896. Don Quixote, Rio de Janeiro, ano 2, n. 60, 4 maio 1896. Disponível em: https://www2.senado.leg.br/bdsf/handle/id/507627.",
    ),
    make_item(
        id="BR-018",
        title="Senhores de escravos pedem indenização à República (Angelo Agostini)",
        date="1888-06-09", year=1888,
        period="Imperial Period (1822–1889)",
        creator="Angelo Agostini",
        institution="Biblioteca Nacional",
        source_archive="Hemeroteca Digital Brasileira",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Marianne", "Abolição", "Indenização"],
        description="Figure of Marianne/Brazilian Republic prominent in the composition. One of the first appearances of Marianne in Revista Illustrada before the Proclamation of the Republic in 1889. Context: abolition of slavery (Lei Áurea, 13/05/1888).",
        url="http://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=332747b",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["pré-Proclamação", "Abolição", "Agostini", "Revista Illustrada", "Marianne"],
        citation_abnt="AGOSTINI, Angelo. [Senhores de escravos pedem indenização à República]. Revista Illustrada, Rio de Janeiro, 9 jun. 1888. Disponível em: http://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=332747b.",
    ),
    make_item(
        id="BR-019",
        title="O tempo passa, mas as datas gloriosas ficam (Angelo Agostini, Don Quixote)",
        date="1895-05-18", year=1895,
        period="Early Republic (1889–1930)",
        creator="Angelo Agostini",
        institution="Senado Federal — BDSF",
        source_archive="Biblioteca Digital do Senado Federal",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Alegoria feminina", "Don Quixote", "Satira"],
        description="Don Quixote salutes the book of the Lei 13 de Maio while holding a sword to defend the female allegory of the Republic from a snake inscribed 'política glicérica'. Sancho kneels beating the snake. The Republic (allegory) looks at the snake with fear, protected in her cloak. Inverts the combative Marianne role — the Republic as victim/protected figure.",
        url="https://www2.senado.leg.br/bdsf/handle/id/507627",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["Don Quixote", "Agostini", "sátira", "República vitimizada", "Abolição"],
        citation_abnt="AGOSTINI, Angelo. O tempo passa, mas as datas gloriosas ficam. Don Quixote, Rio de Janeiro, ano 1, n. 17, p. 8, 18 maio 1895. Disponível em: https://www2.senado.leg.br/bdsf/handle/id/507627.",
    ),
    make_item(
        id="BR-020",
        title="Alegorias da República em A Ventarola (Pelotas, 1887–1889)",
        date="1887–1889", year=1888,
        period="Imperial Period (1822–1889)",
        creator="Unknown (A Ventarola, Pelotas)",
        institution="Biblioteca Pública Pelotense",
        source_archive="Biblioteca Pública Pelotense (não digitalizado)",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Alegoria feminina", "Barrete frígio", "Anti-monarquia"],
        description="Series from the Pelotas illustrated press. (1) 1888: Aged Emperor with heavy crown vs. vigorous young female allegory with Phrygian cap and sword — 'ready for battle'. (2) 1887: Allegory tending a lush plant (Republic) with cap, vs. a dry plant (Empire). Republican woman carries flag inscribed 'porvir' and downward-pointing sword with 'Liberté...'.",
        url="https://cip.brapci.inf.br/download/56493",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["A Ventarola", "Pelotas", "Rio Grande do Sul", "anti-monarquia", "barrete frígio"],
        citation_abnt="ALEGORIAS da República. A Ventarola, Pelotas, 1887–1889. Análise em: LOPES, Aristeu Machado. Disponível em: https://cip.brapci.inf.br/download/56493.",
        scope_note="Acervo na Biblioteca Pública Pelotense, não disponível digitalmente. Análise baseada em reproduções acadêmicas.",
    ),
    make_item(
        id="BR-021",
        title="Diplomas da Exposição Nacional de 1908 — Alegoria da República (Oscar Pereira da Silva)",
        date="1908", year=1908,
        period="Early Republic (1889–1930)",
        creator="Oscar Pereira da Silva (1867–1939)",
        institution="Brasiliana Fotográfica",
        source_archive="Brasiliana Fotográfica",
        country="Brazil", medium="Diploma / Print",
        motif=["República", "Alegoria feminina", "Barrete frígio", "Exposição Nacional"],
        description="Woman in Classical Antiquity garb, Phrygian cap, branches (coffee/olive), left hand on globe highlighting South America, right hand holding the charter of port opening (historical reference). Balanced, centralized, secure representation — Republic as guardian of national identity.",
        url="https://brasilianafotografica.bn.gov.br/?tag=exposicao-nacional-de-1908",
        medium_norm="Estampa", period_norm="República/Império (BR)",
        support="diploma/estampa",
        tags=["Exposição Nacional 1908", "Oscar Pereira da Silva", "barrete frígio", "diploma"],
        citation_abnt="PEREIRA DA SILVA, Oscar. [Diplomas da Exposição Nacional de 1908]. 1908. Disponível em: https://brasilianafotografica.bn.gov.br/?tag=exposicao-nacional-de-1908.",
    ),
    make_item(
        id="BR-022",
        title="A Revolução e seus efeitos (Henrique Fleiuss, Semana Illustrada)",
        date="1869-05-02", year=1869,
        period="Imperial Period (1822–1889)",
        creator="Henrique Fleiuss",
        institution="Biblioteca Nacional",
        source_archive="Hemeroteca Digital Brasileira",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["Anti-alegoria", "Mulher real", "Sátira monárquica"],
        description="Comic strip: husband going to 'the revolution' gets beaten by his wife before being arrested. No classical female allegory employed. The woman appears as a real domestic character, not a symbol. Fleiuss (monarchist) deliberately avoids the republican female allegory to desacralize it. Significant contrast: Fleiuss uses 'real woman' while republican periodicals use the allegory.",
        url="https://memoria.bn.gov.br/DocReader/docreader.aspx?bib=702951&PagFis=4375",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["Semana Illustrada", "Fleiuss", "anti-alegoria", "monarquismo", "controle negativo"],
        citation_abnt="FLEIUSS, Henrique. A Revolução e seus efeitos. Semana Illustrada, Rio de Janeiro, 2 maio 1869. Disponível em: https://memoria.bn.gov.br/DocReader/docreader.aspx?bib=702951&PagFis=4375.",
        scope_note="Controle negativo: ausência deliberada de alegoria feminina por artista monarquista.",
    ),
    make_item(
        id="BR-023",
        title="Duas comadres — A República e A Reforma (A Vida Fluminense, 1872)",
        date="1872", year=1872,
        period="Imperial Period (1822–1889)",
        creator="Unknown",
        institution="Biblioteca Nacional",
        source_archive="Hemeroteca Digital Brasileira",
        country="Brazil", medium="Lithograph (periódico ilustrado)",
        motif=["República", "Reforma", "Alegoria feminina", "Sátira", "Barrete frígio"],
        description="Two corpulent female figures symbolizing the journals A República and A Reforma. A República wears Phrygian cap with caricatured expression. A Reforma wears cap wrapped by crown (ambiguous position: reformism within monarchy). Oversized bodies, exaggerated breasts — sarcastic, non-heroic representation of the allegories. Both in dialogue as 'comadres' (gossips).",
        url="http://memoria.bn.gov.br",
        medium_norm="Estampa/Periódico", period_norm="República/Império (BR)",
        support="periódico ilustrado",
        tags=["A Vida Fluminense", "sátira", "corpo feminino", "caricatura", "barrete frígio"],
        citation_abnt="DUAS comadres. A Vida Fluminense, Rio de Janeiro, 1872. Análise em: LOPES, Aristeu Machado. Disponível em: https://dialnet.unirioja.es/descarga/articulo/10182919.pdf.",
    ),
    make_item(
        id="BR-024",
        title="A Justiça — bronze interior, plenário (Alfredo Ceschiatti, STF)",
        date="1978", year=1978,
        period="Military Dictatorship (1964–1985)",
        creator="Alfredo Ceschiatti (1918–1989)",
        institution="Supremo Tribunal Federal",
        source_archive="STF Memória",
        country="Brazil", medium="Sculpture (bronze)",
        motif=["Justiça", "Têmis", "Alegoria feminina", "Venda"],
        description="Bronze sculpture of seated goddess Themis (Justiça), blindfolded, at the entrance to the Plenário do Tribunal da Constituição. Second, smaller-scale version of the same iconographic program as the exterior granite work (BR-009). Head detail: 50 × 53 × 65 cm. Damaged in January 8, 2023 attack; rescued from STF gardens during restoration.",
        url="https://www.facebook.com/supremotribunalfederal/videos/665682549791145/",
        medium_norm="Escultura", period_norm="Ditadura Militar",
        support="escultura em bronze",
        tags=["Ceschiatti", "STF", "Brasília", "bronze", "Justiça", "January 8"],
        citation_abnt="CESCHIATTI, Alfredo. A Justiça. 1978. 1 escultura, bronze. Supremo Tribunal Federal, Brasília. Referência acadêmica: SILVA, João Balbino. 2019. Dissertação (UnB). Disponível em: https://www.repositorio.unb.br/bitstream/10482/37177/1/2019_JoãoBalbinoSilva.pdf.",
        citation_chicago="Ceschiatti, Alfredo. A Justiça. 1978. Bronze Sculpture. Supremo Tribunal Federal, Brasília. UnB Repository. https://www.repositorio.unb.br/bitstream/10482/37177/1/2019_JoãoBalbinoSilva.pdf.",
    ),
    make_item(
        id="BR-025",
        title="Justiça Sentada (Fábio Mendes, Senado Federal)",
        date="2018", year=2018,
        period="Contemporary (1985–present)",
        creator="Fábio Mendes (n. 1975, Sobradinho)",
        institution="Museu do Senado Federal",
        source_archive="Tainacan Senado",
        country="Brazil", medium="Metal relief",
        motif=["Justiça", "Alegoria feminina", "Balança", "Espada", "Venda"],
        description="Allegorical representation of Justice. Seated woman, eyes covered by blindfold, wearing a dress, seated on papers. Right hand: sword with blade pointing down. Left arm: raised, holding scales. All classic Justitia/Themis attributes present (venda, espada, balança). Dimensions: mancha 25.7 × 21.1 cm, obra 29 × 24.2 cm, moldura 40.6 × 35.8 cm. Signed 'Mendes'. Donated to the Senate.",
        url="https://tainacan.senado.leg.br/acervo/justica-sentada/",
        medium_norm="Escultura/Relevo", period_norm="Contemporâneo",
        support="relevo em metal",
        tags=["Fábio Mendes", "Senado", "Justiça", "balança", "espada", "venda", "contemporâneo"],
        citation_abnt="MENDES, Fábio. Justiça Sentada. 2018. 1 relevo em metal, 29 × 24,2 cm. Museu do Senado Federal, Brasília. Disponível em: https://tainacan.senado.leg.br/acervo/justica-sentada/.",
        citation_chicago="Mendes, Fábio. Justiça Sentada. 2018. Metal Relief, 29 × 24.2 cm. Museu do Senado Federal, Brasília. Tainacan. https://tainacan.senado.leg.br/acervo/justica-sentada/.",
    ),
]

# ─── NEW FRENCH ITEMS ─────────────────────────────────────────────────────

NEW_FR = [
    make_item(
        id="FR-031",
        title="République de Clésinger (Atelier Nadar)",
        date="1900", year=1900,
        period="Third Republic (1870–1940)",
        creator="Atelier Nadar (photographe); Auguste Clésinger (1814–1883), sculpteur",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Photograph (tirage albuminé)",
        motif=["République", "Sculpture", "Allégorie féminine"],
        description="Demonstration photograph by Nadar's atelier of a sculptural allegorical Republic by Auguste Clésinger — female figure in the Third Republic's monumental statuary tradition. Two views: A (ark btv1b531241805) and B (ark btv1b53124181m). 14,5 × 10,5 cm each.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b531241805",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b531241805.highres",
        medium_norm="Fotografia", period_norm="III República / II Império (FR)",
        support="fotografia albuminada",
        tags=["Nadar", "Clésinger", "sculpture", "République", "Third Republic"],
        citation_abnt="ATELIER NADAR. [République de Clésinger]. 1900. 2 fotografias, tiragem albuminada, 14,5 × 10,5 cm. BnF, Estampes et photographie, FT 4-NA-238 (2). Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b531241805.",
        citation_chicago="Atelier Nadar. République de Clésinger. 1900. Albumen Print. Bibliothèque nationale de France. Gallica. https://gallica.bnf.fr/ark:/12148/btv1b531241805.",
    ),
    make_item(
        id="FR-032",
        title="La République (Peynot), Exposition Universelle 1889 (Blancard)",
        date="1889", year=1889,
        period="Third Republic (1870–1940)",
        creator="Hippolyte Blancard (1843–1924), photographe; Émile Peynot (1850–1932), sculpteur",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Photograph (platine)",
        motif=["République", "Sculpture", "Exposition Universelle"],
        description="Photograph of the allegorical statue of the Republic by sculptor Émile Peynot at the 1889 Paris Universal Exposition on the Champ-de-Mars. Platinum print, 22.5 × 16 cm. Companion photographs also exist.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b116003372",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b116003372.highres",
        medium_norm="Fotografia", period_norm="III República / II Império (FR)",
        support="fotografia platina",
        tags=["Blancard", "Peynot", "Exposition Universelle 1889", "sculpture", "République"],
        citation_abnt="BLANCARD, Hippolyte. [La République (Peynot), Exposition Universelle 1889]. 1889. 1 fotografia, tiragem platina, 22,5 × 16 cm. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b116003372.",
    ),
    make_item(
        id="FR-033",
        title="Unité indivisibilité de la République : j'ai rompu mes chaînes vive la liberté",
        date="1793–1794", year=1793,
        period="French Revolution (1789–1799)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte, coloriée)",
        motif=["République", "Liberté", "Force", "Grilhões rompidos"],
        description="Revolutionary placard combining emblems of the Republic with the motto of liberty. Female allegorical figure of Force/République breaking her chains. Grand format (52 × 39.5 cm). Collection de Vinck, vol. 45, pièce 6131.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b6950386s",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b6950386s.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa colorida",
        tags=["Revolution", "chains", "République", "Force", "De Vinck 6131"],
        citation_abnt="UNITÉ indivisibilité de la République. [1793–1794]. 1 gravura, água-forte colorida, 52 × 39,5 cm. BnF, Collection de Vinck, vol. 45, pièce 6131. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b6950386s.",
    ),
    make_item(
        id="FR-034",
        title="Au nom de la République française — passeport (Launay / Gatteaux)",
        date="1798", year=1798,
        period="French Revolution (1789–1799)",
        creator="Robert de Launay (1749?–1814), graveur; Nicolas-Marie Gatteaux (1751–1832), dessinateur",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte, burin)",
        motif=["République", "Paix", "Force", "Document officiel"],
        description="Header vignette for a Republican passport under the Directoire. Allegorical female figure embodying the Republic (with symbols of Peace and Force), framing the official document. 16 × 22 cm. Collection Hennin, tome 138, pièce 12173.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b84125562",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b84125562.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa",
        tags=["Directoire", "passeport", "République", "Hennin 12173"],
        citation_abnt="LAUNAY, Robert de; GATTEAUX, Nicolas-Marie. [Au nom de la République française — passeport]. 1798. 1 gravura, água-forte e buril, 16 × 22 cm. BnF, Collection Hennin, t. 138, pièce 12173. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b84125562.",
    ),
    make_item(
        id="FR-035",
        title="Sept vignettes en-tête de papiers d'administrations (1793)",
        date="1793", year=1793,
        period="French Revolution (1789–1799)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (woodcut / eau-forte)",
        motif=["République", "Justice", "Liberté", "Égalité", "Concorde", "Force", "Espérance"],
        description="Seven allegorical vignettes from letterheads of Revolutionary-era administrations. All major Republican virtues represented in female allegorical form: Force, Justice, Concorde, Liberté, Espérance, Égalité, République. Collection de Vinck, vol. 28, pièce 4817.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b69486542",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b69486542.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="vinheta administrativa",
        tags=["vignettes", "letterhead", "seven virtues", "Revolution", "De Vinck 4817"],
        citation_abnt="SEPT vignettes en-tête de papiers d'administrations. 1793. 7 vinhetas, gravura. BnF, Collection de Vinck, vol. 28, pièce 4817. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b69486542.",
    ),
    make_item(
        id="FR-036",
        title="Nouveau calendrier de la République française, 3e année (Queverdo / Picquet)",
        date="1794", year=1794,
        period="French Revolution (1789–1799)",
        creator="François-Marie-Isidore Queverdo (1748–1797), graveur; Charles Picquet (1771–1827), graveur en lettres",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (gravure)",
        motif=["Justice", "Liberté", "Égalité", "Loi", "Force", "Calendrier républicain"],
        description="Republican calendar for Year III. Rich allegorical composition: female personifications of Justice, Liberté, Égalité, Loi (Law), and Force alongside Revolutionary martyrs (Chalier, Bara, Le Peletier, Marat). Justice holds scales and sword; Liberté holds bonnet phrygien. Hydra of Despotism trampled beneath their feet.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b84123193",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b84123193.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="calendário republicano",
        tags=["calendrier républicain", "Year III", "Queverdo", "five virtues", "Revolution"],
        citation_abnt="QUEVERDO, François-Marie-Isidore; PICQUET, Charles. Nouveau calendrier de la République française, 3e année, 2e semestre. 1794. 1 gravura. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b84123193.",
    ),
    make_item(
        id="FR-037",
        title="[18 mars] — Marianne du mouvement ouvrier (Steinlen, 1894)",
        date="1894", year=1894,
        period="Third Republic (1870–1940)",
        creator="Théophile Alexandre Steinlen (1859–1923)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Lithograph",
        motif=["Marianne", "Mouvement ouvrier", "Commune de Paris"],
        description="Steinlen's socialist Marianne commemorating the Paris Commune (18 March anniversary). Marianne leading or accompanying the working class — workers, artists, demonstrators. A social-republican reading distinct from official propaganda. 41.4 × 34.7 cm. Ref: Crauzat 143.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b53188502h",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b53188502h.highres",
        medium_norm="Gravura/Estampe", period_norm="III República / II Império (FR)",
        support="litografia",
        tags=["Steinlen", "Commune", "socialist Marianne", "mouvement ouvrier", "Crauzat 143"],
        citation_abnt="STEINLEN, Théophile Alexandre. [18 mars]. 1894. 1 litografia, 41,4 × 34,7 cm. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b53188502h.",
    ),
    make_item(
        id="FR-038",
        title="Liberté (Moitte / Janinet, 1792)",
        date="1792", year=1792,
        period="French Revolution (1789–1799)",
        creator="Jean-François Janinet (1752–1814), graveur; Jean-Guillaume Moitte (1746–1810), dessinateur",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (technique mixte)",
        motif=["Liberté", "Despotisme", "Force"],
        description="One of the most canonical Revolutionary representations of Liberté as a female allegorical figure. Designed by sculptor Moitte and engraved by Janinet. She stands victorious over Despotism. Refs: IFF18 Janinet 156; Portalis-Béraldi Janinet 108; De Vinck 6050–6051; Hennin 11793.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b100269179",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b100269179.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa",
        tags=["Liberté", "Moitte", "Janinet", "canonical", "Revolution", "Hennin 11793"],
        citation_abnt="MOITTE, Jean-Guillaume; JANINET, Jean-François. Liberté. 1792. 1 gravura. BnF, Estampes et photographie, RESERVE EF-105 (3)-FOL. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b100269179.",
    ),
    make_item(
        id="FR-039",
        title="La Liberté, soutenue par la Raison, protège l'Innocence & couronne la Vertu (Boizot / Bernier)",
        date="1793–1795", year=1793,
        period="French Revolution (1789–1799)",
        creator="François Bernier, graveur; Louis-Simon Boizot (1743–1809), dessinateur",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte)",
        motif=["Liberté", "Raison", "Innocence", "Vertu", "Force"],
        description="Large-format allegorical print. Liberté (standing female figure with bonnet phrygien and sceptre) supported by Raison (Reason) and protecting Innocence while crowning Vertu (Virtue). Fully developed Revolutionary allegorical program. 36.5 × 53 cm. Ref: Hennin 12177.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b84125599",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b84125599.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa",
        tags=["Boizot", "Liberté", "Raison", "Revolution", "Hennin 12177"],
        citation_abnt="BOIZOT, Louis-Simon; BERNIER, François. La Liberté, soutenue par la Raison, protège l'Innocence & couronne la Vertu. [1793–1795]. 1 gravura, água-forte, 36,5 × 53 cm. BnF. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b84125599.",
    ),
    make_item(
        id="FR-040",
        title="La Liberté armée du Sceptre de la Raison foudroye l'Ignorance et le Fanatisme (Boizot / Chapuy)",
        date="1793–1795", year=1793,
        period="French Revolution (1789–1799)",
        creator="Jean-Baptiste Chapuy (1760–18..), graveur; Louis-Simon Boizot (1743–1809), dessinateur",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte, burin, pointillé)",
        motif=["Liberté", "Raison", "Ignorance", "Fanatisme"],
        description="Companion piece to FR-039 (Boizot series). Liberté armed with the Sceptre of Reason strikes down Ignorance and Fanaticism. Powerful, striding female figure in antique drapery with bonnet phrygien. 44.5 × 58.5 cm. Ref: Hennin 12178.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b69450527",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b69450527.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa",
        tags=["Boizot", "Chapuy", "Liberté", "Raison", "Revolution", "Hennin 12178"],
        citation_abnt="BOIZOT, Louis-Simon; CHAPUY, Jean-Baptiste. La Liberté armée du Sceptre de la Raison foudroye l'Ignorance et le Fanatisme. [1793–1795]. 1 gravura, 44,5 × 58,5 cm. BnF. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b69450527.",
    ),
    make_item(
        id="FR-041",
        title="La Liberté ou la mort (vignette, Garde nationale de Lyon)",
        date="1793–1794", year=1793,
        period="French Revolution (1789–1799)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte, burin)",
        motif=["Liberté", "Force", "Garde nationale"],
        description="Revolutionary vignette for the Lyon National Guard with the motto 'La Liberté ou la mort.' Female figure of Liberté with trophies of arms (fasces, weapons). Small format (10.5 × 23 cm) — likely letterhead vignette. Collection de Vinck, vol. 28.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b6948658q",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b6948658q.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="vinheta administrativa",
        tags=["Lyon", "Garde nationale", "Liberté ou la mort", "Revolution"],
        citation_abnt="LA LIBERTÉ ou la mort. [1793–1794]. 1 vinheta, água-forte e buril, 10,5 × 23 cm. BnF, Collection de Vinck, vol. 28. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b6948658q.",
    ),
    make_item(
        id="FR-042",
        title="La Liberté dictant ses loix aux Nations (Didier)",
        date="1793–1794", year=1793,
        period="French Revolution (1789–1799)",
        creator="Didier (graveur)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte, pointillé)",
        motif=["Liberté", "Force", "Constitution 1793", "Marat", "Le Peletier"],
        description="Liberté dictating laws to the Nations. Grandiose composition: Liberté as robed female figure holding the Constitution of 1793, directing the nations, flanked by monuments to Revolutionary martyrs. 34.5 × 27.5 cm. Collection de Vinck.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b6949899n",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b6949899n.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa",
        tags=["Liberté", "Constitution 1793", "nations", "martyrs", "Revolution"],
        citation_abnt="DIDIER. La Liberté dictant ses loix aux Nations. [1793–1794]. 1 gravura, água-forte e pontilhado, 34,5 × 27,5 cm. BnF, Collection de Vinck. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b6949899n.",
    ),
    make_item(
        id="FR-043",
        title="Droits de l'homme — Déclaration avec Liberté, Justice, Concorde, Force (Beuvelot)",
        date="1789–1792", year=1789,
        period="French Revolution (1789–1799)",
        creator="Beuvelot (marchand d'estampes)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving",
        motif=["Liberté", "Justice", "Concorde", "Force", "Déclaration des droits"],
        description="Allegorical frontispiece to the Declaration of the Rights of Man and Citizen. Female figures of Liberté, Justice, Concorde, and Force surround the text within a portico/arch framework. Canonical Revolutionary print with multiple allegorical registers. Collection de Vinck.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b69480436",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b69480436.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa",
        tags=["Déclaration des droits", "four virtues", "frontispiece", "Revolution"],
        citation_abnt="BEUVELOT. [Droits de l'homme — Déclaration des droits de l'homme et du citoyen]. [1789–1792]. 1 gravura. BnF, Collection de Vinck. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b69480436.",
    ),
    make_item(
        id="FR-044",
        title="Tableau allégorique de la restauration de la liberté des Français (1790)",
        date="1790", year=1790,
        period="French Revolution (1789–1799)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte coloriée)",
        motif=["France", "Liberté", "Renommée", "Despotisme", "Louis XVI"],
        description="'La France assise sur un lion...' Allegorical tableau of France as female figure enthroned on a lion, presiding over the restoration of liberty. Renommée (Fame) and allegorical geniuses surround her, with Despotisme trampled below. Includes portrait of Louis XVI. Collection de Vinck.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b6941865c",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b6941865c.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa colorida",
        tags=["France", "lion", "Renommée", "Louis XVI", "Revolution"],
        citation_abnt="TABLEAU allégorique de la restauration de la liberté des Français. 1790. 1 gravura, água-forte colorida. BnF, Collection de Vinck. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b6941865c.",
    ),
    make_item(
        id="FR-045",
        title="Trois vignettes en-tête de papiers d'administrations (1790)",
        date="1790", year=1790,
        period="French Revolution (1789–1799)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving",
        motif=["Liberté", "Force"],
        description="Three vignettes from letterheads of Revolutionary-era administrations. Female personifications of Liberté with Force. Collection de Vinck.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b6948614j",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b6948614j.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="vinheta administrativa",
        tags=["vignettes", "letterhead", "Liberté", "Force", "Revolution"],
        citation_abnt="TROIS vignettes en-tête de papiers d'administrations. 1790. 3 vinhetas, gravura. BnF, Collection de Vinck. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b6948614j.",
    ),
    make_item(
        id="FR-046",
        title="Les Amis de la Constitution aux manes de Mirabeau — France éplorée (Lélu, 1791)",
        date="1791", year=1791,
        period="French Revolution (1789–1799)",
        creator="Pierre Lélu (1741–1810)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving",
        motif=["France", "Liberté", "Renommée", "Immortalité", "Mirabeau"],
        description="Commemorative allegory of Mirabeau's death. France personified as an 'éplorée' (weeping female figure), joined by Liberté, Renommée (Fame), and Immortalité around the monument to the great orator. Classic funeral/commemorative allegory with female figures.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b6943142k",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b6943142k.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa",
        tags=["Mirabeau", "France éplorée", "funeral allegory", "Lélu", "Revolution"],
        citation_abnt="LÉLU, Pierre. Les Amis de la Constitution aux manes de Mirabeau. 1791. 1 gravura. BnF, Collection de Vinck. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b6943142k.",
    ),
    # ── Pre-1789 items (included fully per Ana's decision) ──
    make_item(
        id="FR-047",
        title="[Les sept vertus] Justicia (Bruegel / Galle, 1559)",
        date="1559–1560", year=1559,
        period="Early Modern (pre-1789)",
        creator="Philippe Galle (1537–1612), graveur; Pieter Bruegel l'Ancien (1525?–1569), dessinateur",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (burin)",
        motif=["Justice", "Seven Virtues", "Tribunal"],
        description="One of the most important Northern Renaissance allegories. Bruegel's 'Justicia' from his series of the Seven Virtues, engraved by Philippe Galle. Justice is a female figure holding sword and scales, surrounded by a courthouse scene of legal proceedings. 25.9 × 32.2 cm. Refs: New Hollstein, Pieter Bruegel the Elder, 16; Lebeer 34.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b100213982",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b100213982.highres",
        medium_norm="Gravura/Estampe", period_norm="Antigo Regime / Pré-moderno",
        support="estampa (buril)",
        tags=["Bruegel", "Galle", "Seven Virtues", "Justicia", "Renaissance", "New Hollstein 16"],
        citation_abnt="BRUEGEL, Pieter, o Velho; GALLE, Philippe. [Les sept vertus] Justicia. 1559–1560. 1 gravura, buril, 25,9 × 32,2 cm. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b100213982.",
    ),
    make_item(
        id="FR-048",
        title="[La Justice] — gravure en bois (16e siècle)",
        date="15..–1584", year=1570,
        period="Early Modern (pre-1789)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Woodblock print",
        motif=["Justice"],
        description="Large woodblock print of Justice as a female figure in 16th-century French style. Grand format (400 × 510 mm) suggests broadside or decorative use. Classical attributes (scales, sword) expected.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b55001927d",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b55001927d.highres",
        medium_norm="Gravura/Estampe", period_norm="Antigo Regime / Pré-moderno",
        support="xilogravura",
        tags=["Justice", "woodblock", "16th century", "broadside"],
        citation_abnt="[LA JUSTICE]. [15..–1584]. 1 xilogravura, 400 × 510 mm. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b55001927d.",
    ),
    make_item(
        id="FR-049",
        title="B Justicia XXXVII (Ladenspelder, after Master of the Die)",
        date="1540–1560", year=1550,
        period="Early Modern (pre-1789)",
        creator="Johann Ladenspelder (16th c.); after Maître aux dés",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (burin)",
        motif=["Justice", "Cardinal Virtues"],
        description="Engraved allegory of Justicia numbered XXXVII in a series. German engraver Ladenspelder after the 'Master of the Die' (anonymous Italian designer active c. 1530–60). Classical female Justice figure.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b105495868",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b105495868.highres",
        medium_norm="Gravura/Estampe", period_norm="Antigo Regime / Pré-moderno",
        support="estampa (buril)",
        tags=["Ladenspelder", "Master of the Die", "Justicia", "Renaissance", "series"],
        citation_abnt="LADENSPELDER, Johann. B Justicia XXXVII. [1540–1560]. 1 gravura, buril. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b105495868.",
    ),
    make_item(
        id="FR-050",
        title="[La Justice entre la Charité et la Force] — dessin néerlandais (c. 1710)",
        date="c. 1710", year=1710,
        period="Early Modern (pre-1789)",
        creator="Anonyme des Pays-Bas, XVIIe siècle",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Drawing (dessin)",
        motif=["Justice", "Charité", "Force"],
        description="Drawing (Dutch school) of the triadic allegorical group: Justice flanked by Charity and Force. Canonical Renaissance/Baroque scheme. Justice holds scales and sword; Charity holds a child or heart; Force holds fasces or a column.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b53240455t",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b53240455t.highres",
        medium_norm="Desenho", period_norm="Antigo Regime / Pré-moderno",
        support="desenho",
        tags=["Dutch school", "triadic allegory", "Justice", "Charité", "Force", "Baroque"],
        citation_abnt="[LA JUSTICE entre la Charité et la Force]. c. 1710. 1 desenho. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b53240455t.",
    ),
    make_item(
        id="FR-051",
        title="[Allégories des vertus — La Justice] (Baptiste Pellerin, 1560–1570)",
        date="1560–1570", year=1565,
        period="Early Modern (pre-1789)",
        creator="Baptiste Pellerin (attrib.)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Drawing (encre et lavis)",
        motif=["Justice", "Cardinal Virtues"],
        description="Drawing by Baptiste Pellerin from an allegorical virtues series. Justice as a female figure in 16th-century French/Fontainebleau style with sword and scales.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b53234029x",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b53234029x.highres",
        medium_norm="Desenho", period_norm="Antigo Regime / Pré-moderno",
        support="desenho (tinta e aguada)",
        tags=["Pellerin", "Fontainebleau", "Justice", "virtues series", "Renaissance"],
        citation_abnt="PELLERIN, Baptiste (atrib.). [Allégories des vertus — La Justice]. [1560–1570]. 1 desenho, tinta e aguada. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b53234029x.",
    ),
    make_item(
        id="FR-052",
        title="Allégorie en l'honneur de Jules Mazarin — Justice et Prudence (Huret, 1645–1660)",
        date="1645–1660", year=1650,
        period="Early Modern (pre-1789)",
        creator="Grégoire Huret (1606–1670)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (burin)",
        motif=["Justice", "Prudence", "Force", "Modération", "Mazarin"],
        description="Allegorical portrait of Cardinal Mazarin surrounded by female allegories: Justice, Force, Modération, and Prudence. Classical Baroque allegorical program. Justice holds sword and scales, Prudence holds mirror and serpent. 32.1 × 40 cm.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b53254750d",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b53254750d.highres",
        medium_norm="Gravura/Estampe", period_norm="Antigo Regime / Pré-moderno",
        support="estampa (buril)",
        tags=["Huret", "Mazarin", "four virtues", "Baroque", "political allegory"],
        citation_abnt="HURET, Grégoire. [Allégorie en l'honneur de Jules Mazarin]. [1645–1660]. 1 gravura, buril, 32,1 × 40 cm. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b53254750d.",
    ),
    make_item(
        id="FR-053",
        title="Allégorie en l'honneur de Louis XIII — Justice et Prudence (Huret, 1640–1643)",
        date="1640–1643", year=1641,
        period="Early Modern (pre-1789)",
        creator="Grégoire Huret (1606–1670)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (burin)",
        motif=["Justice", "Prudence", "Force", "Modération", "Louis XIII"],
        description="Royal allegorical portrait-frontispiece of Louis XIII surrounded by cardinal/royal virtues: Justice, Prudence, Force, Modération. Companion work to Mazarin allegory (FR-052). Includes reference to the Siege of La Rochelle (1627–28). 33.5 × 22.5 cm.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b8402182w",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b8402182w.highres",
        medium_norm="Gravura/Estampe", period_norm="Antigo Regime / Pré-moderno",
        support="estampa (buril)",
        tags=["Huret", "Louis XIII", "royal virtues", "Baroque", "La Rochelle"],
        citation_abnt="HURET, Grégoire. [Allégorie en l'honneur de Louis XIII]. [1640–1643]. 1 gravura, buril, 33,5 × 22,5 cm. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b8402182w.",
    ),
    make_item(
        id="FR-054",
        title="Conseil exécutif provisoire — décret avec Justice (vignettes, 1793–1794)",
        date="1793–1794", year=1793,
        period="French Revolution (1789–1799)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte)",
        motif=["Justice", "Force"],
        description="Small-format Republican letterhead with Justice and Force as allegorical header vignettes for official correspondence of the Provisional Executive Council. Three views/states. 7.5 × 9 cm.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b8412239h",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b8412239h.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="vinheta administrativa",
        tags=["Conseil exécutif", "Justice", "Force", "letterhead", "Revolution"],
        citation_abnt="CONSEIL exécutif provisoire — décret de la Convention nationale. [1793–1794]. 3 vinhetas, água-forte, 7,5 × 9 cm. BnF. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b8412239h.",
    ),
    make_item(
        id="FR-055",
        title="[Les sept vertus — La Justice] CON FRINGE (école flamande, 1547)",
        date="1547", year=1547,
        period="Early Modern (pre-1789)",
        creator="Unknown (école flamande?)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving",
        motif=["Justice", "Seven Virtues"],
        description="Mid-16th-century print with inscription CON FRINGE.EOS.VIRGA FE[RREA] ('Break them with a rod of iron') — Psalm-derived motto for Justice. Female allegorical figure of Justice in 16th-century dress.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b53250287h",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b53250287h.highres",
        medium_norm="Gravura/Estampe", period_norm="Antigo Regime / Pré-moderno",
        support="estampa",
        tags=["Flemish school", "Seven Virtues", "Justice", "Psalm", "1547"],
        citation_abnt="[LES SEPT VERTUS — La Justice]. 1547. 1 gravura. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b53250287h.",
    ),
    make_item(
        id="FR-056",
        title="La Révolution française — double state avec Justice, Liberté, Égalité (1792–1793)",
        date="1792–1793", year=1792,
        period="French Revolution (1789–1799)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (eau-forte coloriée)",
        motif=["Vérité", "Justice", "Liberté", "Égalité", "Force", "Fraternité", "Paix"],
        description="Large allegorical prints summarizing the French Revolution as a female allegorical program. Multiple female figures representing all Revolutionary virtues. Two states (1792 and 1793) differ in inscriptions. ARKs: btv1b69429317 (1792), btv1b6942930t (1793). A richly documented pair.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b69429317",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b69429317.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="estampa colorida",
        tags=["Revolution", "seven virtues", "double state", "1792", "1793"],
        citation_abnt="LA RÉVOLUTION française. [1792–1793]. 2 gravuras (estados), água-forte colorida. BnF, Collection de Vinck. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b69429317.",
    ),
    make_item(
        id="FR-057",
        title="Almanach national dédié aux amis de la Constitution (1790)",
        date="1790", year=1790,
        period="French Revolution (1789–1799)",
        creator="Unknown",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Engraving (almanach)",
        motif=["Liberté", "Force", "Constitution"],
        description="Allegory of the Constitution on a pedestal, with female personifications of Liberté and Force flanking it. Almanach format.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b8411294d",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b8411294d.highres",
        medium_norm="Gravura/Estampe", period_norm="Revolução Francesa",
        support="almanaque",
        tags=["almanach", "Constitution", "Liberté", "Force", "1790"],
        citation_abnt="ALMANACH national dédié aux amis de la Constitution. 1790. 1 gravura. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b8411294d.",
    ),
    make_item(
        id="FR-058",
        title="La polka des cathédrales (Jean Veber, 1911)",
        date="1911", year=1911,
        period="Third Republic (1870–1940)",
        creator="Jean Veber (1864–1928)",
        institution="Bibliothèque nationale de France",
        source_archive="Gallica",
        country="France", medium="Print (impression photomécanique)",
        motif=["Marianne", "Satire", "Séparation Église-État"],
        description="Satirical political cartoon. Marianne in a dance ('polka') with the cathedrals — satirizing clerical/Republican tensions of the Third Republic under the Separation law.",
        url="https://gallica.bnf.fr/ark:/12148/btv1b8577688t",
        thumbnail_url="https://gallica.bnf.fr/ark:/12148/btv1b8577688t.highres",
        medium_norm="Gravura/Estampe", period_norm="III República / II Império (FR)",
        support="estampa",
        tags=["Veber", "Marianne", "Séparation", "satire", "cathedrals"],
        citation_abnt="VEBER, Jean. [La polka des cathédrales]. 1911. 1 estampa. BnF, Estampes et photographie. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b8577688t.",
    ),
]

ALL_NEW = NEW_BR + NEW_FR


# ─── SCOUT NOTE GENERATION ────────────────────────────────────────────────

def generate_scout_note(item):
    """Generate a SCOUT note markdown string for a corpus item."""
    country_code = "BR" if item["country"] == "Brazil" else "FR"
    support_tag = item.get("support", "desconhecido") or "desconhecido"
    main_motif = (item["motif"][0] if item["motif"] else "alegoria-feminina").lower().replace(" ", "-")

    tags_yaml = "\n".join(f'  - {t}' for t in [
        "corpus/candidato",
        f"pais/{country_code}",
        f"suporte/{support_tag.replace(' ', '-')}",
        f"motivo/{main_motif}",
    ])

    status = "imagem-pendente" if not item.get("thumbnail_url") else "verificar"

    note = f"""---
id: {item['id']}
tipo: corpus/candidato
status: {status}
titulo: "{item['title']}"
pais: {item['country']}
periodo: "{item['date']}"
tags:
{tags_yaml}
fonte_analise: {SOURCE}
data_analise: {TODAY}
related:
  - "[[corpus-data]]"
---

## {item['title']}

**ID**: {item['id']} | **País**: {item['country']} | **Data**: {item['date']}
**Suporte**: {item.get('medium', 'Unknown')} | **Instituição**: {item.get('institution', 'Unknown')}
**Arquivo**: {item.get('source_archive', 'Unknown')}

### Descrição

{item.get('description', 'Pending analysis.')}

### Metadados do corpus

**Motivos**: {item.get('motif_str', '')}
**Tags**: {item.get('tags_str', '')}
**URL**: {item.get('url', '')}
"""
    return note


def safe_filename(item):
    """Generate a safe filename for a SCOUT note."""
    title = item["title"][:60].rstrip()
    # Remove chars unsafe for filenames
    for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        title = title.replace(c, '')
    return f"{item['id']} {title}.md"


# ─── MAIN ─────────────────────────────────────────────────────────────────

def main():
    apply = "--apply" in sys.argv
    gen_notes = "--notes" in sys.argv

    # Load corpus
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    existing_ids = {item["id"] for item in corpus}
    print(f"Loaded corpus: {len(corpus)} items")

    # ── Phase 1: Enrichments ──
    enriched_count = 0
    for item in corpus:
        if item["id"] in ENRICHMENTS:
            enrich = ENRICHMENTS[item["id"]]
            for key, val in enrich.items():
                if key == "_merge_description":
                    existing = item.get("description") or ""
                    if val not in existing:
                        item["description"] = f"{existing} [Gallery enrichment: {val}]"
                        enriched_count += 1
                elif key == "thumbnail_url":
                    if not item.get("thumbnail_url"):
                        item[key] = val
                        enriched_count += 1
                else:
                    if not item.get(key):
                        item[key] = val
                        enriched_count += 1

    print(f"Enriched {enriched_count} fields across {len(ENRICHMENTS)} existing items")

    # ── Phase 2: New items ──
    new_count = 0
    skipped = []
    for item in ALL_NEW:
        if item["id"] in existing_ids:
            skipped.append(item["id"])
            continue
        corpus.append(item)
        existing_ids.add(item["id"])
        new_count += 1

    print(f"New items to add: {new_count}")
    if skipped:
        print(f"Skipped (already exist): {skipped}")

    # ── Phase 3: Validate ──
    ids = [item["id"] for item in corpus]
    dups = [x for x in ids if ids.count(x) > 1]
    if dups:
        print(f"ERROR: Duplicate IDs found: {set(dups)}")
        sys.exit(1)

    br_count = sum(1 for i in corpus if i["id"].startswith("BR"))
    fr_count = sum(1 for i in corpus if i["id"].startswith("FR"))
    print(f"\nCorpus totals: {len(corpus)} items (BR={br_count}, FR={fr_count})")

    if apply:
        # Write corpus
        with open(CORPUS_PATH, "w") as f:
            json.dump(corpus, f, indent=2, ensure_ascii=False)
        print(f"\nWritten to {CORPUS_PATH}")

        if gen_notes:
            # Generate SCOUT notes
            VAULT_DIR.mkdir(parents=True, exist_ok=True)
            notes_written = 0
            for item in ALL_NEW:
                if item["id"] in [s for s in skipped]:
                    continue
                fname = safe_filename(item)
                fpath = VAULT_DIR / fname
                if not fpath.exists():
                    note = generate_scout_note(item)
                    fpath.write_text(note, encoding="utf-8")
                    notes_written += 1
            print(f"SCOUT notes written: {notes_written}")
    else:
        print("\nDRY RUN — pass --apply to write changes, --apply --notes for notes too")


if __name__ == "__main__":
    main()
