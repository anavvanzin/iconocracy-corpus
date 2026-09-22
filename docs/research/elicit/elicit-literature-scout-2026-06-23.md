---
title: "Elicit literature scout — ICONOCRACY, penal history, administrative law"
date: 2026-06-23
source: "Elicit API /api/v1/search"
status: "raw search results + triage; citations not yet Zotero-verified"
---

# Elicit literature scout — 2026-06-23

This file records the second Elicit API literature-scout batch requested by Ana on 2026-06-23. It is a working research note, not a final bibliography.

Security note: the Elicit key is stored only in the Hermes environment as `ELICIT_API_KEY`; it is not written in this repository.

## Run metadata

- Tool: `Elicit API /api/v1/search`
- Requests: 5
- Endpoint status: all five queries returned HTTP 200
- Search quota remaining after this batch: 89
- Reports were not created; this batch used search only.
- Citation warning: Elicit metadata is useful for discovery but must be verified in Zotero / DOI / publisher pages before thesis use.

## Executive synthesis

1. The Brazil thesis search strongly supports treating Brazil as the anchor rather than one country among six: the strongest hits cluster around First Republic public-building allegories, “Marianne à brasileira”, positivist civic architecture, and elite visual discourse.
2. The France/Britain search supports controlled comparison: Marianne/France for sovereignty and legality; Britannia/Britain for foundation-of-law imagery and national personification. It does not justify expanding the core beyond the Brazil–France–Great Britain triangle.
3. The penal-history searches did not recover Maria Gonçalves Cajada directly, but they did surface a strong procedural-gender-race route: Portuguese Inquisition procedure, witness secrecy/insufficiency, confession, colonial transplantation, and women accused of feitiçaria.
4. The administrative-law search found a usable Brazilian article spine: explicabilidade, contraditório algorítmico, motivação, transparência, LGPD review of automated decisions, LAI, and democratic oversight.

## Query-level triage

### Brazil thesis — Primeira República / alegoria feminina / edifícios públicos / raça

- Query: `"Primeira República" alegoria feminina República Brasil iconografia edifícios públicos raça`
- Status: 200
- Returned papers: 8

Triage:

Keep / prioritize:
- ENTRE MARIANNE E CLOTILDE
- Visual culture in Brazil's First Republic (1889–1930): allegories and elite discourse
- Marianne à brasileira: imagens republicanas e os dilemas do passado imperial
- PAÇO DOS AÇORIANOS: A ESTÉTICA RELIGIOSA DO POSITIVISMO CASTILHISTA NA PRIMEIRA REPÚBLICA (1889-1930)

Maybe / contextual:
- BIBLIOTECA, O NACIONAL E A MODERNIDADE NA BELLE ÉPOQUE CARIOCA
- MÜLLER, Maria Lúcia Rodrigues. A cor da escola: imagens da Primeira República. Cuiabá: EDUFMT/Entrelinhas, 2008
- Ideários da Educação Feminina na Primeira República Brasileira
- Liberdade, igualdade e democracia: o ideário republicano e a educação das mulheres no início do século XX no Brasil

Interpretive note:
- Strong confirmation that the Brazil chapter should use republican public-building allegory and “Marianne à brasileira” as core bibliography. Education/women items are contextual only unless used to frame the social non-emancipation behind the symbolic woman.

### France/Britain comparators — Marianne / Britannia / sovereignty / law

- Query: `Marianne Britannia allegory sovereignty republican iconography law state`
- Status: 200
- Returned papers: 8

Triage:

Keep / prioritize:
- Marianne into battle: Republican imagery and symbolism in France 1789–1880
- The Allegorical Image of France, 1750-1800: A Political Crisis of Representation
- Liberté, Légalité, Souveraineté: Changing Meanings of an Allegory in Le Barbier’s Representations of the Déclaration des droits de l’Homme et du citoyen
- Imagining the Foundations of Law in Britain: Magna Carta in 2015
- Britannia and Melita: Pseudomorphic Sisters

Maybe / contextual:
- La matrona y el león: imágenes de la nación liberal en la España del Siglo XIX
- Iconography of the Labour Movement. Part 1: Republican Iconography, 1792–1848
- Kongebilleder

Interpretive note:
- France/Britain remain best used as controlled comparators for sovereignty, legality and national iconography. Spain/Malta/socialist iconography can support genealogical diffusion but should not expand the country core.

### Penal article — Maria Gonçalves Cajada / feitiçaria / processo criminal

- Query: `"Maria Gonçalves Cajada" feitiçaria processo criminal Brasil colonial`
- Status: 200
- Returned papers: 8

Triage:

Keep / prioritize:
- Feitiçaria na vila de Curitiba: direito e misoginia (xviii)
- Feitiçaria paulista: transcrição de processo-crime da Justiça Eclesiástica na América portuguesa do século XVIII
- Luzia Soares, processada por feitiçaria pelo Tribunal da Inquisição de Lisboa: uma análise histórica- jurídica
- GÊNERO E MORALIDADE NA SALVADOR SEISCENTISTA: O CASO DE MARIA BARBOSA (1600-1614)

Maybe / contextual:
- Práticas de feitiçaria no Brasil Estudo de caso de duas feiticeiras acusadas no Grão-Pará no Século XVIII
- Com quantos medos se constrói uma bruxa? Misoginia e demonização da mulher no Brasil Colonial.
- Ídolo, feitiço e pacto: a Inquisição portuguesa e a religiosidade centro-africana em Lisboa no século XVIII: o caso de Maria de Jesus
- Violência e Resistência. um estudo de caso a partir do processo inquisitorial de Maria da Cruz (1593)

Interpretive note:
- No exact Maria Gonçalves Cajada hit appeared in this Elicit batch. That is itself useful: the article should not rely on Elicit alone for that case; search ANTT/BN/Google Scholar/SciELO/Periódicos CAPES and local notes next.

### Penal method gate — Portuguese Inquisition / witchcraft / evidence / confession

- Query: `Portuguese Inquisition witchcraft criminal procedure Brazil colonial evidence confession`
- Status: 200
- Returned papers: 8

Triage:

Keep / prioritize:
- Andanças da Inquisição no Brasil
- Inquisição no Brasil: Modus operandi dos inquisidores do Tribunal do Santo Oficio de Lisboa nos processos envolvendo à colônia (1640 - 1739)
- The Trial of Íria Álvares: Conviviality and Inequality in the Portuguese Inquisition Records
- Africans, Afro-Brazilians and Afro-Portuguese in the Iberian Inquisition in the seventeenth and eighteenth centuries
- Feitiçaria paulista: transcrição de processo-crime da Justiça Eclesiástica na América portuguesa do século XVIII

Maybe / contextual:
- Na Teia do Inquisidor: Povos Indígenas do Brasil e a Inquisição Portuguesa
- Atuação inquisitorial no Brasil
- Bento Teixeira: Inquisição e Sociedade Colonial

Interpretive note:
- Best route for the penal article: evidentiary procedure, witness insufficiency, secrecy of accusations, confession, colonial transplantation, and race/gendered defendants. This is stronger than a generic “Malleus in Brazil” frame.

### Admin Brazil — ADM algorítmica / LGPD / LAI / Lei 14.129 / devido processo

- Query: `administração pública algoritmo decisão automatizada LGPD LAI Lei 14.129 devido processo administrativo`
- Status: 200
- Returned papers: 8

Triage:

Keep / prioritize:
- Explicabilidade e contraditório algorítimico nas decisões automatizadas no setor público: as decisões em processos apoiados em algoritmos e o problema da redução da realidade a dados
- Big data, algoritmos e inteligência artificial na administração pública: reflexões para a sua utilização em um ambiente democrático
- Decisões algorítmicas na Administração Pública: entre a opacidade técnica e o dever de transparência
- A sujeição às decisões automatizadas a partir da Lei Geral de Proteção de Dados
- O dilema ético da decisão algorítmica

Maybe / contextual:
- ADMINISTRAÇÃO ALGORÍTMICA E PROCESSO LEGAL: IMPACTOS DA AUTOMATIZAÇÃO SOBRE A TRANSPARÊNCIA, A MOTIVAÇÃO E O CONTROLE INSTITUCIONAL
- DEVIDO PROCESSO DIGITAL E CONSTITUCIONALISMO ALGORÍTMICO: LIMITES, TRANSPARÊNCIA E CONTROLE DEMOCRÁTICO NO USO DE INTELIGÊNCIA ARTIFICIAL PELO PODER PÚBLICO
- GOVERNANÇA ALGORÍTMICA NAS COMPRAS PÚBLICAS: UM ESTUDO SOBRE AS OPORTUNIDADES DA IA E OS RISCOS DE VIÉS (BIAS) E OPACIDADE DECISÓRIA

Interpretive note:
- Brazil-specific administrative-law literature exists. Article spine should be: explicability + contraditório + motivation + transparency + review of automated decisions, then connect LGPD/LAI/Lei 14.129/2021 and procurement/governance as specific domains.

## Full returned results

### Brazil thesis — Primeira República / alegoria feminina / edifícios públicos / raça

1. ENTRE MARIANNE E CLOTILDE — 2022 — Francisco De Assis de Sousa Nascimento; Joel Marcos Brasil de Sousa Batista — DOI: 10.32748/revec.v8i21.18508
   - Venue: Revista de Estudos de Cultura
   - Abstract/summary excerpt: O presente artigo visa analisar as representações republicanas imagéticas da mulher, como símbolo do regime republicano, fabricadas durante os primeiros anos da República (1889–1896) e como estavam relacionadas com a realidade da mulher; somado com essa análise foram investigadas as semelhanças e diferenças dessas representações simbólicas, com os modelos da propaganda da república francesa. A pergunta norteadora deste artigo foi: por que a representação feminina ter sido construída como símbolo na propaganda republicana? Foram utilizadas como fontes históricas: pinturas de La liberté guidant le peuple (1831), La Republique (1848), Glória e Pátria da Revista Ilustrada (1889) e Alegoria da República (1896).Palavras-chave: Brasil Republicano; Símbolos; Mulher.

2. Ideários da Educação Feminina na Primeira República Brasileira — 2019 — Renata Patricia Forain de Valentim; R. Martins; Mariana Martelo Rodrigues — DOI: 10.1590/18094449201900570006
   - Venue: Cadernos Pagu
   - Abstract/summary excerpt: Resumo Partindo das propostas políticas e científicas que nortearam os caminhos da Primeira República brasileira, duas questões inter-relacionadas se projetaram nesta pesquisa: resgatar as ideias básicas relacionadas à educação e à instrução da mulher, que começavam a se institucionalizar no Rio de Janeiro, e compreender os diferentes graus de adesão desse ideário pedagógico às formulações normatizadoras, higiênicas e eugênicas, que construíram o discurso hegemônico no período.

3. PAÇO DOS AÇORIANOS: A ESTÉTICA RELIGIOSA DO POSITIVISMO CASTILHISTA NA PRIMEIRA REPÚBLICA (1889-1930) — 2019 — W. Wachholz; André Daniel Reinke; M. R. Saldanha — DOI: 10.22351/nepp.v45i1.3858
   - Venue: Protestantismo em Revista
   - Abstract/summary excerpt: O positivismo do Rio Grande do Sul desenvolveu caracteristicas que lhe renderam a alcunha de “castilhista”, especialmente em funcao dos ditames de seu maior representante, Julio Prates de Castilhos. Enquanto a Republica brasileira construia seu imaginario simbolico no centro do pais, Castilhos coordenava em Porto Alegre a construcao da sede da intendencia da capital, o Paco dos Acorianos, em cuja arquitetura aplicou principios esteticos que exaltavam os aspectos autoritarios da Republica por ele defendida. Esse artigo analisa as caracteristicas religiosas de seu discurso arquitetonico e escultural, as quais demonstram os objetivos de construir um imaginario e legado politico messiânico por parte daquele que foi chamado “Patriarca” do Rio Grande do Sul.

4. Visual culture in Brazil's First Republic (1889–1930): allegories and elite discourse — 2006 — Valéria Salgueiro — DOI: 10.1111/J.1469-8129.2006.00239.X
   - Venue: Nations and Nationalism
   - Abstract/summary excerpt: ABSTRACT. The research on which the present work is based analyses the ornamentation of the facades of major Brazilian public buildings and investigates how that representation contributed to the construction of a visual national identity during Brazil's First Republic (1889–1930). Two government buildings are discussed: Pedro Ernesto Palace, inaugurated in 1923 to house the municipal chamber of Rio de Janeiro, and Tiradentes Palace, erected in the years 1922–26 to house Brazil's Parliament. The article focuses on the allegorical figures ornamenting these two buildings in order to explore contradictory aspects of the discourse they convey. It will be argued that visual culture, more precisely architecture and architectural sculpture, served the elites of this period as a powerful tool for projecting their values and for preventing contradictions within Brazilian society from emerging in

5. Liberdade, igualdade e democracia: o ideário republicano e a educação das mulheres no início do século XX no Brasil — 2018 — L. Oliveira; V. L. Martiniak — DOI: 10.25053/REDUFOR.V3I9.861
   - Venue: Educação Formação
   - Abstract/summary excerpt: O presente artigo tem como objetivo apresentar uma reflexão acerca da influência dos ideais liberais na educação das mulheres no contexto da Primeira República brasileira (1889-1930). A pesquisa, de caráter bibliográfica, fundamenta-se em livros, artigos e publicações científicas que apresentam reflexões diante do tema proposto neste estudo. A discussão aqui apresentada prioriza a relação da educação com os fatores econômicos, políticos e sociais, já que se compreende que o objeto de pesquisa não pode ser entendido como uma situação isolada. Constatou-se que os ideais liberais influenciaram o discurso de que a educação seria para todos, entretanto, a entrada das mulheres nesse campo, se deu de forma lenta e distinta. A República não visava a emancipação econômica, política e nem o pleno desenvolvimento feminino.

6. MÜLLER, Maria Lúcia Rodrigues. A cor da escola: imagens da Primeira República. Cuiabá: EDUFMT/Entrelinhas, 2008 — 2012 — Lucia Maria Assunção Barbosa — DOI: 10.29286/REP.V18I38.400
   - Venue: Revista de Educação Pública
   - Abstract/summary excerpt: A cor da escola: imagens da Primeira República, de Maria Lúcia Rodrigues Muller2, é um livro que, tal como propõe o título, expõe 54 fotografias de estudantes e professores negros com o objetivo de mostrar a presença desses docentes em escolas públicas dos estados do Rio de Janeiro e de Mato Grosso, no período de 1889 a 1930.

7. Marianne à brasileira: imagens republicanas e os dilemas do passado imperial — 2020 — Lima Junior.; Carlos Rogério — DOI: 10.11606/T.93.2020.TDE-16062021-151518
   - Abstract/summary excerpt: \n A Proclamação da República, em 15 de novembro de 1889, ensejou a produção de uma nova visualidade para a nação. Por meio de um levantamento de pinturas históricas, retratos e alegorias encontrados em museus e arquivos de São Paulo, Minas Gerais, Rio de Janeiro, Bahia, Pará e Amazonas, mas também suas reproduções impressas e gravadas em litografias (jornais, revistas e panfletos), produzidas nos primeiros tempos republicanos, esta investigação pretende demonstrar como se deu a criação de símbolos e imagens com vistas a promover uma legitimação visual do poder republicano em tensão com a imagética do regime imperial. A análise atenta do corpus de imagens levantadas demonstrou que, diferentemente do que se podia supor, as imagens da República não suplantam totalmente as do Império. Pelo contrário, há muitas sobrevivências dos símbolos do regime anterior naquele que passa a vigorar. Para

8. BIBLIOTECA, O NACIONAL E A MODERNIDADE NA BELLE ÉPOQUE CARIOCA — 2021 — Carlos Henrique Juvêncio — DOI: 10.14295/biblos.v35i1.12304
   - Venue: Biblos
   - Abstract/summary excerpt: O final do século XIX e o início do século XX representam para o Rio de Janeiro, e para o Brasil um momento de profundas transformações políticas, sociais e urbanas. Num contexto de intensa agitação político-social graças à Proclamação da República, a Biblioteca Nacional emerge como uma das grandes beneficiadas dos movimento de modernização da antiga capital do país. Este artigo objetiva compreender como a Biblioteca Nacional se tornou símbolo da Primeira República e nela se ancora a consagração do regime republicano. Posiciona a BN como um espaço representante do moderno, seja em suas práticas, arquitetura ou no capital social que acumula ao seu redor. Concluí que a Biblioteca Nacional exerce o seu papel de guardiã da memória nacional, além de oferecer o moderno através de seus produtos e serviços e ser um polo de erudição em busca do desejo de civilização e modernidade da Primeira Repú

### France/Britain comparators — Marianne / Britannia / sovereignty / law

1. Marianne into battle: Republican imagery and symbolism in France 1789–1880 — 1982 — D. Outram — DOI: 10.1016/0191-6599(82)90025-0
   - Venue: History of European Ideas
   - Abstract/summary excerpt: n/a

2. The Allegorical Image of France, 1750-1800: A Political Crisis of Representation — 1994 — Antoine de Baecque — DOI: 10.2307/2928788
   - Venue: Representations
   - Abstract/summary excerpt: A FI GURE: AN I DEA . The allegorical mode of representation and the uses of metaphorical analogy that define it are precious objects to the historian of representations, particularly when studying the end of the eighteenth century-a period when, among the modes of representation, allegory seemed the most suited to the incarnation of political sovereignty. Allegory expressed a crucial visual narrative: it told the story of political power through metaphor, through a figurative correspondence between material things and the discourse of ideas. Surrounding and reflecting the body of the king, and later carrying the emblems of revolutionary power, indeed embodying this power through the incarnation of revolutionary values, allegory was recognized as critically important in contemporary political and aesthetic debates, both by artists working for the monarchy and by republican engravers and

3. Liberté, Légalité, Souveraineté: Changing Meanings of an Allegory in Le Barbier’s Representations of the Déclaration des droits de l’Homme et du citoyen — 2024 — Frank Ejby Poulsen — DOI: 10.6035/potestas.7824
   - Venue: Potestas. Estudios del Mundo Clásico e Historia del Arte
   - Abstract/summary excerpt: This article analyzes three visual works representing the 1789 Declaration of the Rights of Man attributed to Le Barbier: two paintings and one engraving. The article makes the hypothesis that one painting was executed shortly after the Declaration in August 1789, while the other was made after the engraving, dated November 5, 1790. Treating visual works as texts and combining methods in art history and intellectual history, the article’s main argument is that the two paintings express different narratives and thereby different views on sovereignty. Identifying the right allegory as a genius figure of liberty, the first painting presents her annunciating the Supreme Being’s natural rights to monarchical France. The engraving erroneously claims the allegory to be the Law, while the setting is changed and the scepter points to the Supreme Being, thereby giving legitimate sovereignty to the

4. Kongebilleder — 2022 — David Hasberg Zirak-Schmidt — DOI: 10.7146/kok.v50i133.132739
   - Venue: K&amp;K - Kultur og Klasse
   - Abstract/summary excerpt: This article analyses a conflict between royalist iconography and republican iconoclasm in the visual strategies of the frontispieces to Eikon Basilike and Eikon Alethine, two works that react to the execution of Charles I in 1649. The article argues that the clash between these two visual strategies is emblematic of a clash between a republican and an absolutist notion of sovereignty current in Caroline England. The absolutist notion of sovereignty may be meaningfully approached through Walter Benjamin’s theory of the ambiguous nature of early modern sovereignty. For Benjamin, the early modern sovereign is simultaneously a tyrant and a martyr. This double nature of the figure of the sovereign is the result of early modern political theology. The republican notion of sovereignty, which develops in the 1640s, is characterized by its emphasis on popular sovereignty. According to this view,

5. La matrona y el león: imágenes de la nación liberal en la España del Siglo XIX — 2010 — J. Fuentes
   - Abstract/summary excerpt: This article takes a unique look at how the Liberal State of nineteenth century Spain was constructed, focusing on symbolism and allegory, specifically on how the iconography of the Matron and the Lion was officially adopted by the Democratic Sexenio Regime (1868-1874). As with most symbolic discourse, it was a slow process, whereby the iconography of the old monarchy was progressively transferred onto the idea of sovereign nation, finally culminating into the symbolism of the Republic. This article gives a full account of the changes undergone in the symbolic syntax of the Matron and Lion iconography and how these changes were influenced by the historical circumstances in which they took place

6. Imagining the Foundations of Law in Britain: Magna Carta in 2015 — 2017 — Martin A. Kayman — DOI: 10.1017/S2071832200021994
   - Venue: German Law Journal
   - Abstract/summary excerpt: The 800th anniversary of Magna Carta offers a study in how the foundations of law have been visualized in the United Kingdom. The fact that the British sense of identity as a free nation has historically been based on its commitment to “unwritten” law means that it lacks a foundational text and has hence traditionally figured the law through a plurality of images without a core. The absence of a singular image on which to focus national identity became acute in the early twenty-first century as the multiplication of sources of legality and justice in a globalized and multicultural world put pressure on the United Kingdom's sense of sovereignty. The tensions manifest in this crisis can be seen across a range of images produced for the anniversary, each bearing different values. Yet the rival narratives are able to coexist in the same commemorative space, their differences subsumed within

7. Iconography of the Labour Movement. Part 1: Republican Iconography, 1792–1848 — 2020 — Fred Andersson — DOI: 10.69945/ico.vi1-2.25660
   - Venue: Nordic Review of Iconography
   - Abstract/summary excerpt: This is the first article in a two-part study of the background and development of the iconography of the international socialist labour movement. With the breakthrough of modern political ideologies after the American and French revolutions, the symbols of freemasonry long remained an important point of reference for new iconographic systems serving secular propagandistic needs. The virtues and vices of classical moral education were replaced or combined with new ones, and old symbols were invested with altered meanings in the context of political satire and allegory. The human and especially the female body retained prominence as a vehicle for conceptual personification in official display and in the minds of common people. After September 21, 1792 (the abolition of the French monarchy), the attempt to replace Christian religion with a cult of the Goddess of Liberty and other associate

8. Britannia and Melita: Pseudomorphic Sisters — 1996 — Derk Kinnane-Roelofsma — DOI: 10.2307/751401
   - Venue: Journal of the Warburg and Courtauld Institutes
   - Abstract/summary excerpt: robably the best-known allegorical figures are personifications of countries. Uncle Sam is the stock in trade of cartoonists worldwide, as are Britannia and France's Marianne. Uncle Sam is a modern figure, essentially a representative type-Aby Warburg even fancied he sighted him walking the streets of San Francisco.' But even if Marianne is the product of revolutionary upheaval, she still has some connection with ancient antecedents.2 Britannia has a long past involving significant changes in her appearance. Even more complex is the history of a Britannia look-alike, Melita, the embodiment of the Mediterranean nation of Malta

### Penal article — Maria Gonçalves Cajada / feitiçaria / processo criminal

1. GÊNERO E MORALIDADE NA SALVADOR SEISCENTISTA: O CASO DE MARIA BARBOSA (1600-1614) — 2019 — H. Silva — DOI: 10.13102/semic.v0i22.3911
   - Venue: Anais dos Seminários de Iniciação Científica
   - Abstract/summary excerpt: O presente trabalho está inserido na área de História, no campo da História Cultural, bem como dos estudos de gênero, e tem como principal objeto de pesquisa o processo inquisitorial movido contra Maria Barbosa, mulher parda – por vezes descrita como mulata por suas/seus delatoras/es –, vendedora de pão, natural de Évora, moradora da Baía de Todos os Santos, casada com o ourives João da Cruz e filha de pais pardos forros De acordo com testemunhas que a denunciaram, Maria Barbosa saiu de Évora degredada para Angola pelo crime de feitiçaria. Em Angola açoitaram-na publicamente por ser feiticeira e alcoviteira e novamente a degredaram, dessa vez, para Pernambuco, onde de acordo com os denunciantes também “levava mal caminho”, passando depois a viver em Salvador, terra onde foi presa em 1612 por ordem do Bispo do Brasil D. Constantino Barradas que a considerava mulher “notoriamente a mais pr

2. Feitiçaria na vila de Curitiba: direito e misoginia (xviii) — 2019 — Danielle Regina Wobeto de Araujo — DOI: 10.1590/2179-8966/2018/31930
   - Venue: Revista Direito e Práxis
   - Abstract/summary excerpt: Resumo Traçaremos a relação feitiçaria e mulheres no período colonial brasileiro por meio de um processo criminal secular que apurou o delito de feitiçaria na Vila de Curitiba, da segunda metade do Século XVIII. O percurso do texto partiu de um panorama geral da “caça às bruxas” na Europa, distinguindo as particularidades em Portugal, comparando a feitiçaria metropolitana e a colonial e averiguando a mentalidade misógina na Colônia.

3. Feitiçaria paulista: transcrição de processo-crime da Justiça Eclesiástica na América portuguesa do século XVIII — 2018 — Narayan Pereira Porto — DOI: 10.11606/D.8.2019.tde-02052019-112854
   - Abstract/summary excerpt: The present thesis aims to offer the semidiplomatic transcription and philological analysis of an inquisitorial lawsuit started by the Ecclesiastical Court from So Paulo, in 1754, in Jundia, in which the defendants, Thereza Leyte and Escholastica Pinta da Sylva (mother and daughter), are accused of killing Escholastica's first husband by means of witchcraft. They are also accused of killing other men and of having a pact with the devil. The research also seeks to contribute to elucidate the means through which the Holy Office acted in Europe and in Portuguese America, with the objective of enlightening its actuation in colonial Brazil. Furthermore, a codicological and paleographic study of the documentation is presented, approaching aspects related to the paper used, the inks, the abbreviation system and other aspects related to the Portuguese language writing in the 18 th century. At th

4. Violência e Resistência. um estudo de caso a partir do processo inquisitorial de Maria da Cruz (1593) — 2023 — M. Campos — DOI: 10.29327/1283294.7-106
   - Venue: Anais do(a) Congresso Internacional de Direitos Humanos de Coimbra
   - Abstract/summary excerpt: estruturaram a sociedade colonial brasileira (FREYRE, 2013).

5. Luzia Soares, processada por feitiçaria pelo Tribunal da Inquisição de Lisboa: uma análise histórica- jurídica — 2022 — Isabela De Andrade Pena Miranda Corby — DOI: 10.22478/ufpb.1982-6605.2021v18n2.61286
   - Venue: Religare
   - Abstract/summary excerpt: O presente artigo analisa o processo de Luzia Soares, escrava crioula, acusada por feitiçaria, cujo procedimento fora iniciado pelo juízo ordinário, pelo Vigário da Vara de Ribeirão do Carmo, em 1738, e finalizado pela mesa da Inquisição em 1745. Trata-se de um caso estudado por diversos pesquisadores, visto que é envolto de peculiaridades, as quais desembocam na absolvição de Luzia. Esta pesquisa tem como objetivo acrescentar às análises já realizadas anteriormente a percepção de que havia uma prudência procedimental do Tribunal da Inquisição e, para tanto, era observado o sistema de produção de provas. Além disso, reiteramos por novos ângulos que a absolvição de Luzia ocorreu em virtude de um conjunto de vícios procedimentais. Na metodologia de análise, utilizamos uma perspectiva jurídica para interpretação da fonte. Observamos que antes de adentrar no exame do caso, propomos algumas c

6. Com quantos medos se constrói uma bruxa? Misoginia e demonização da mulher no Brasil Colonial. — 2019 — C. R. Silva — DOI: 10.5380/CRA.V19I2.61722
   - Venue: Revista de Antropologia
   - Abstract/summary excerpt: Durante toda Idade Média e Moderna o tema da natural inclinação feminina para os comportamentos desviantes fazia parte do programa educacional de padres e religiosos das mais variadas ordens. Os médicos também reafirmaram em seus escritos a inferioridade física e moral das mulheres, e os juristas, igualmente, deram sua contribuição para reforçar a inferioridade estrutural do sexo feminino. A produção literária e a iconografia da Renascença foram da mesma forma hostis à condição feminina. Esse artigo resgata a história de duas escravas mestiças, Joana e Custódia de Abreu, que assumiram participar de encontros noturnos firmados por pactos diabólicos no Piauí colonial. Mulheres mestiças, descendentes de escravos africanos e indígenas, pobres e imersas numa sociedade misógina, opressora e extremamente híbrida, com interconexão de cultos e culturas diversas, de origem africana, indígena e eur

7. Práticas de feitiçaria no Brasil Estudo de caso de duas feiticeiras acusadas no Grão-Pará no Século XVIII — 2022 — Gilmara Cruz de Araújo — DOI: 10.14482/memor.47.364.18
   - Venue: Memorias
   - Abstract/summary excerpt: Este artigo tem objetivo de esmiuçar e refletir sobre as Práticas Rituais de duas mulheres acusadas de feitiçaria na região do Grão-Pará setecentista. Visa a uma análise mais aprofundada sobre as práticas mágicas de cura – consideradas pela Inquisição como feitiçaria – e a formação de uma cul-tura muitas vezes negada e demonizada pela visão europeia. As mulheres consideradas feiticeiras foram alvos de perseguições e personagens ativas na História do Grão-Pará (Brasil) no Período Co-lonial, o que contribuiu para a formação de uma nova identidade (múltipla) cultural na colônia. Para tal, a análise será realizada através dos documentos inquisitoriais sobre Ludovina Ferreira e da índia Sabina. Esses documentos são relativos à Visitação do Santo Ofício da Inquisição ao local entre os anos 1763-1769, e estão sob a guarda do Arquivo Nacional da Torre do Tombo (ANTT), em Lisboa (Portugal), mas f

8. Ídolo, feitiço e pacto: a Inquisição portuguesa e a religiosidade centro-africana em Lisboa no século XVIII: o caso de Maria de Jesus — 2019 — Josinaldo Sousa de Queiroz; Priscila Gusmão de Andrade; Rômulo Nascimento — DOI: 10.23925/1677-1222.2018VOL19I1A12
   - Venue: REVER - Revista de Estudos da Religião
   - Abstract/summary excerpt: O presente artigo tem por objetivo discutir um processo inquisitorial contra a angolana Maria de Jesus, que foi presa e julgada pelo Tribunal do Santo Ofício pelo suposto crime de “pacto com o demônio” em Lisboa, no ano de 1735. Para tanto, utilizamos bibliografia clássica e atual sobre o tema, para compreender, a partir do olhar da ré, quais os motivos a levaram a realizar tal prática e o que isto representava na cultura católica e centro-africana.

### Penal method gate — Portuguese Inquisition / witchcraft / evidence / confession

1. Feitiçaria paulista: transcrição de processo-crime da Justiça Eclesiástica na América portuguesa do século XVIII — 2018 — Narayan Pereira Porto — DOI: 10.11606/D.8.2019.tde-02052019-112854
   - Abstract/summary excerpt: The present thesis aims to offer the semidiplomatic transcription and philological analysis of an inquisitorial lawsuit started by the Ecclesiastical Court from So Paulo, in 1754, in Jundia, in which the defendants, Thereza Leyte and Escholastica Pinta da Sylva (mother and daughter), are accused of killing Escholastica's first husband by means of witchcraft. They are also accused of killing other men and of having a pact with the devil. The research also seeks to contribute to elucidate the means through which the Holy Office acted in Europe and in Portuguese America, with the objective of enlightening its actuation in colonial Brazil. Furthermore, a codicological and paleographic study of the documentation is presented, approaching aspects related to the paper used, the inks, the abbreviation system and other aspects related to the Portuguese language writing in the 18 th century. At th

2. Andanças da Inquisição no Brasil — 2024 — Nilo Batista — DOI: 10.1590/2179-8966/2023/71158
   - Venue: Revista Direito e Práxis
   - Abstract/summary excerpt: Resumo Concebido como a segunda parte de uma aula sobre Inquisição moderna (a primeira está publicada em Capítulos de Política Criminal, Rio, 2022, ed. Revan, pp. 71 ss), o texto contém um estudo dos procedimentos da Inquisição portuguesa, particularmente das disputas relacionadas à (in)suficiência da testemunha única e à ignorância em que os acusados eram mantidos acerca da identidade das testemunhas e das circunstâncias de seus depoimentos, ressaltando-se as funções místicas então atribuídas à confissão. Registradas três aculturações que favoreceram o transplante da mentalidade inquisitorial sobre os povos originários e mais tarde sobre as culturas africanas para cá desterradas, o texto se detém sobre as quatro Visitações que o Santo Ofício empreendeu no Brasil. Por fim, confissões e delações produzidas nessas Visitações fornecem a matéria prima para conhecermos nossas blasfêmias e as

3. Na Teia do Inquisidor: Povos Indígenas do Brasil e a Inquisição Portuguesa — 2021 — Luana Souto Cavalcanti — DOI: 10.53528/geoconexes.v2i1.37
   - Venue: Geoconexões online
   - Abstract/summary excerpt: O presente artigo tem como objetivo revisitar a Inquisição Portuguesa durante a sua atuação no Brasil Colonial e analisar como esta instituição, se comportou perante as possíveis heresias cometidas pelos povos indígenas entre os séculos XVIII e XIX no Brasil Colônia. Utilizamos para nortear a nossa pesquisa as reflexões metodológicas empreendidas por Carlo Ginzburg para análise de documentos inquisitoriais, revisões bibliográficas de autores que trabalham esta temática e analise de processo crime inquisitorial pertencente ao Arquivo Nacional da Torre do Tombo (ANTT) disponibilizados em formato digital no site do referido Arquivo.

4. Inquisição no Brasil: Modus operandi dos inquisidores do Tribunal do Santo Oficio de Lisboa nos processos envolvendo à colônia (1640 - 1739) — 2022 — José Rubens Lima Jardilino; Mario Gomes Ferreira — DOI: 10.19053/20275137.n25.2022.11382
   - Venue: History and Memory
   - Abstract/summary excerpt: Este artigo trata da Inquisição no Brasil e a atuação dos inquisidores no modus operandi processual do tribunal eclesiástico do Santo Oficio em Lisboa. Os documentos fontes indicam parte do que foi a inquisição portuguesa no Brasil no processo de colonização do território. Busca-se compreender o rito processual por meio da atuação dos inquisidores, topo da organização hierárquica do Santo Oficio da Inquisição Portuguesa. Para tal, se fez necessária à análise de fontes documentais como regimentos, manual de inquisidores, e processos de réus acusados por diversos crimes no tribunal de Lisboa. O estudo foi realizado a partir de fontes primárias e ilustrado por um caso na colônia brasileira, além de fornecer dados sobre os variados processos, julgados no tribunal do Santo Ofício de Lisboa, uma vez que a colônia portuguesa na América não teve tribunal próprio. Espera-se que esse estudo abra c

5. The Trial of Íria Álvares: Conviviality and Inequality in the Portuguese Inquisition Records — 2023 — Jessica O'Leary — DOI: 10.46877/oleary.2023.58
   - Abstract/summary excerpt: In this paper, I analyse the Inquisition trial record of Íria Álvares (fl. 1580-1600), an Indigenous woman from the sertão of Bahia. Íria was the only Indigenous woman born to Indigenous parents who was tried by the First Visit of the Inquisition to Brazil in the sixteenth century. For this reason, her trial record represents a unique opportunity to explore the experiences of a freed Indigenous woman who spent her childhood in the sertão and adolescence and adulthood in colonial society. An analysis of her trial suggests that Íria was cognisant of the dynamics of colonial society and used her understanding of idealised convivialities to her advantage when negotiating the legal apparatus of the Portuguese Inquisition.

6. Bento Teixeira: Inquisição e Sociedade Colonial — 2012 — E. Ribeiro
   - Venue: WebMosaica
   - Abstract/summary excerpt: O artigo analisa, a partir dos depoimentos de Bento Teixeira, reu da Inquisicao Portuguesa, parte da trajetoria deste poeta, cristao-novo, preso em 1595, na capitania de Pernambuco. Os textos que redigiu nos quatro anos em que esteve preso possibilitam-nos conhecer um pouco de sua mentalidade, inserida no contexto colonial brasileiro e na inseguranca e dualidade em que vivia a populacao conversa. Remetem-nos tambem ao cotidianodos carceres do Santo Oficio, descrevendo o tratamento dado aos reus e a corrupcao que grassava no seu interior. Bento Teixeira: Inquisition and colonial society - Abstract: This article analyses part of the trajectory of the New Christian poet Bento Teixeira, defendant of the Portuguese Inquisition, arrested in 1595 in the captaincy of Pernambuco, based on his testimony. The texts written by him during his captivity allow us to know about his mentality, inserted i

7. Atuação inquisitorial no Brasil — 2012 — Gileade Godoi — DOI: 10.20396/lil.v15i29.8664742
   - Venue: Linguas e instrumentos linguísticos
   - Abstract/summary excerpt: Taking as corpus of analysis the book of confessions and denunciations from the last visitation of the Holy Office of the Inquisition made to the colonial state of Grão-Pará and Maranhão, this article reflects on how the visitations of the Holy Office to colonial Brazil, with its prescriptions and proscriptions, mobilized the process of identifying a Brazilian subject, and in this process,how intercontinental memories became part of this subject through transference, resistance, and redefinition.

8. Africans, Afro-Brazilians and Afro-Portuguese in the Iberian Inquisition in the seventeenth and eighteenth centuries — 2012 — Vanicléia Silva Santos — DOI: 10.1080/17528631.2012.629434
   - Venue: African and Black Diaspora: An International Journal
   - Abstract/summary excerpt: The object of this article is to analyze aspects of seventeenth- and eighteenth-century African culture in the Lusophone Atlantic through new methodological approaches to Portuguese inquisitorial sources. The records of the Inquisition are beginning to serve the needs of historians beyond their original functions as religious documentation. The text examines the confessions of Africans prosecuted or denounced for practices of sorceries provide new insights about the evolution of Afro-Atlantic culture. In this paper, I demonstrate that Africans incorporated elements of the popular Catholicism to reinforce specific aspects of their native or non-Catholic cosmogonies.

### Admin Brazil — ADM algorítmica / LGPD / LAI / Lei 14.129 / devido processo

1. Explicabilidade e contraditório algorítimico nas decisões automatizadas no setor público: as decisões em processos apoiados em algoritmos e o problema da redução da realidade a dados — 2024 — André Afonso Tavares; Caroline Müller Bitencourt; José Sérgio da Silva Cristóvam — DOI: 10.36113/dike.27.2024.4556
   - Venue: Diké - Revista Jurídica
   - Abstract/summary excerpt: Diante da produção cada vez mais crescente de decisões automatizadas, sejam intermediárias ou finais, durante processos administrativos ou judiciais, o presente trabalho tem enquanto problema de pesquisa: de que forma as decisões automatizadas, em observância ao princípio da publicidade, estão sendo explicadas, isto é, tem sua lógica de programação tornada pública e transparente? Além disso, em razão da necessidade de se respeitar o princípio do contraditório, uma vez que essas decisões automatizadas podem afetar direitos ou ocasionar obrigações, de que forma se tem garantido aos interessados o direito de influenciar o resultado do processamento algorítmico? O objetivo geral consiste em investigar de que forma as decisões automatizados no âmbito de processos administrativos e judiciais que se apoiam em algoritmos têm buscado oferecer explicabilidade em respeito ao princípio da publicidad

2. Big data, algoritmos e inteligência artificial na administração pública: reflexões para a sua utilização em um ambiente democrático — 2020 — Valter Shuenquener de Araújo; Bruno Almeida Zullo; M. Torres — DOI: 10.21056/aec.v20i80.1219
   - Abstract/summary excerpt: O presente trabalho tem por objetivo analisar o impacto de decisoes administrativas tomadas com base em algoritmos a partir de bancos de dados de grande porte ( Big Data ) no âmbito da Administracao Publica. Sera realizado um mapeamento das potencialidades e desafios inerentes a utilizacao de processos decisorios nao humanos pelo Poder Publico. Com base nisto, sera possivel identificar algumas perplexidades que podem surgir a partir do descompasso entre o avanco tecnologico e o instrumental teorico a disposicao da doutrina administrativista. Nesse cenario, buscaremos problematizar algumas questoes referentes aos contornos que serao atribuidos a discricionariedade administrativa nos casos em que a tomada de decisao publica se de por meio de algoritmos. A metodologia adotada sera bibliografica, descritiva e tera como objetivo investigar o processo decisorio fundamentado em bancos de dados

3. DEVIDO PROCESSO DIGITAL E CONSTITUCIONALISMO ALGORÍTMICO: LIMITES, TRANSPARÊNCIA E CONTROLE DEMOCRÁTICO NO USO DE INTELIGÊNCIA ARTIFICIAL PELO PODER PÚBLICO — 2026 — Leandro Sales — DOI: 10.63391/yzzyr729
   - Venue: International Integralize Scientific
   - Abstract/summary excerpt: A incorporação de sistemas de inteligência artificial pelo Poder Público redefine a arquitetura decisória estatal ao introduzir mecanismos automatizados baseados em modelagem estatística e aprendizado de máquina. Esse cenário tensiona garantias estruturantes do Estado Democrático de Direito, especialmente o devido processo legal, o dever de motivação das decisões, a transparência administrativa e o controle jurisdicional. O presente artigo investiga quais limites constitucionais condicionam a utilização estatal de sistemas algorítmicos no contexto brasileiro. Parte-se da hipótese de que a ausência de deveres reforçados de explicabilidade, auditabilidade, rastreabilidade e revisão humana significativa compromete a racionalidade pública e produz déficit democrático estrutural. A pesquisa adota metodologia qualitativa, de natureza jurídico-dogmática e jurisprudencial, com análise sistemátic

4. O dilema ético da decisão algorítmica — 2022 — André Felipe Silva Puschel; Roberto Tessis Rodrigues; Vivian Cristina Lima López Valle — DOI: 10.21056/aec.v22i90.1737
   - Venue: A&amp;C - Revista de Direito Administrativo &amp; Constitucional
   - Abstract/summary excerpt: A utilização da inteligência artificial como suporte à tomada de decisão é realidade no cenário atual. Discussões sobre processamento de dados - sejam estas por meio de aprendizagem supervisionada, sejam por aprendizagem não supervisionada (deep learning) - ganham relevância no âmbito do direito. Ao mesmo tempo que ganham relevância, porém, surgem os desafios sobre as resultantes que se apresentam em razão do processamento de dados (output), na medida em que estes podem estar enviesados em função do conjunto de dados (dataset) provenientes do mundo físico, das concepções e das relações humanas. Por conta destes desafios, o presente artigo tem por finalidade pontuar tais aspectos no contexto contemporâneo e propor medidas que possam ser adotadas como possíveis soluções. A análise acerca da existência de um antídoto como contraposição ao enviesamento faz-se necessária, no intuito de qualif

5. ADMINISTRAÇÃO ALGORÍTMICA E PROCESSO LEGAL: IMPACTOS DA AUTOMATIZAÇÃO SOBRE A TRANSPARÊNCIA, A MOTIVAÇÃO E O CONTROLE INSTITUCIONAL — 2025 — Jackline Leite de Oliveira; Ivoneide Pereira de Alencar — DOI: 10.69849/revistaft/fa10202508131918
   - Venue: Revista ft
   - Abstract/summary excerpt: The incorporation of algorithm-based technologies into Public Administration has profoundly transformed state decision-making logic, generating significant impacts on transparency, the motivation behind administrative acts, and institutional oversight. While promising gains in efficiency and standardization, so-called algorithmic administration raises tensions between technical rationality and the democratic foundations of the legal process. This study examines the legal and administrative implications of automated decision-making, focusing on the risks of opacity, the weakening of the motivation behind actions, and the limitations of traditional oversight mechanisms. The research adopts a qualitative methodology, based on a literature review and theoretical-legal analysis, articulating contributions by Frank Pasquale on algorithmic opacity, Oscar Vilhena Vieira and Luís Roberto Barroso

6. Decisões algorítmicas na Administração Pública: entre a opacidade técnica e o dever de transparência — 2025 — Amanda de Souza Maia — DOI: 10.47975/ijdl.v6.1297
   - Venue: International Journal of Digital Law
   - Abstract/summary excerpt: O presente artigo examina a incorporação de sistemas algorítmicos na Administração Pública brasileira à luz do dever constitucional de transparência, identificando as barreiras impostas pela opacidade dos modelos complexos de inteligência artificial e as exigências de explicabilidade, interpretabilidade e inteligibilidade. Por meio de pesquisa qualitativa de caráter bibliográfico, foram analisados doutrina, relatórios técnicos e instrumentos normativos — notadamente o PL 2.338/2023, a PEC 29/2023 e o Regulamento Europeu de IA (AI Act) — para identificar limitações do paradigma tradicional de transparência. Os resultados indicam que a efetividade da transparência algorítmica depende da articulação entre normas claras e tecnologia, de modo que os dados estejam não apenas disponíveis, mas também compreensíveis — permitindo que as pessoas acessem, entendam e usem essas informações para acomp

7. A sujeição às decisões automatizadas a partir da Lei Geral de Proteção de Dados — 2020 — Mariah Ferrari Pires; A. Bufulin — DOI: 10.24862/rcdu.v11i1.1224
   - Venue: Revista do Curso de Direito do UNIFOR
   - Abstract/summary excerpt: É notório o crescente controle da vida humana a partir de decisões automatizadas. Elas estão presentes na escolha do candidato ideal para a vaga de emprego, no custo do medicamento a ser adquirido pelo consumidor e até mesmo no possível crédito a ser concedido pelo banco. Referidos exemplos básicos geram grande impacto na vida dos cidadãos, todavia são desprovidos de transparência no tocante ao seu funcionamento, isto é, aos critérios utilizados para a tomada dessas decisões. Esta ausência de transparência, também denominada de opacidade dos algoritmos, gera a ocorrência de práticas abusivas e discriminatórias. Logo, a fim de atenuar tais efeitos, as legislações acerca da proteção de dados pessoais buscaram assegurar o direito à transparência e da não sujeição às decisões automatizadas. Esse artigo aborda, em linhas gerais, o que seria o direito à revisão de decisões automatizadas e como

8. GOVERNANÇA ALGORÍTMICA NAS COMPRAS PÚBLICAS: UM ESTUDO SOBRE AS OPORTUNIDADES DA IA E OS RISCOS DE VIÉS (BIAS) E OPACIDADE DECISÓRIA — 2026 — Juliana Colombelli Candido; Ravena de Oliveira e Almeida Silva; Rodrigo Lima Bandeira — DOI: 10.69849/revistaft/ma10202601161036
   - Venue: Revista ft
   - Abstract/summary excerpt: A Administração Pública brasileira, buscando maior eficiência e probidade, encontra na Inteligência Artificial (IA) e na Governança Algorítmica uma ferramenta promissora para otimizar os processos de licitações e contratos. Não obstante o claro fomento legal à inovação presente na Constituição Federal (Art. 218) e na legislação infraconstitucional (Art. 11, Lei nº 14.133/2021), a delegação de poder decisório a algoritmos introduz novos desafios ético-jurídicos. O presente artigo analisa a dialética entre as oportunidades da IA – como a otimização de custos e a mitigação de fraudes – e os riscos inerentes à sua aplicação, com destaque para o viés (bias) em datasets de treinamento e a opacidade decisória (black box). A metodologia empregada é a dedutiva, baseada em pesquisa bibliográfica e análise do arcabouço normativo, incluindo a LGPD (Art. 20, Lei nº 13.709/2018) e a LAI (Lei nº 12.527

## Next actions

1. Verify the KEEP items in Zotero or publisher pages; do not cite from Elicit metadata alone.
2. For the thesis: add Salgueiro, Carlos Rogério Lima Junior, and “Entre Marianne e Clotilde” to the Brazil bibliography review queue.
3. For the penal article: search the specific Maria Gonçalves Cajada case outside Elicit; use Elicit hits for procedural and gender/race framing.
4. For the administrative-law article: build a two-column matrix: garantia administrativa tradicional → equivalent algorithmic-control requirement.
5. Optional next Elicit step: create one report only after Ana chooses a target article/workstream, because reports may consume workflow quota.
