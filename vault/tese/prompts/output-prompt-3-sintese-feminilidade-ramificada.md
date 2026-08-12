# Output — Prompt 3: Síntese "Feminilidade de Estado Ramificada"
**Data:** 20 de Julho de 2026  
**Status:** Concluído (reescrito pelo agente pai após falha categórica do subagente `deleg_c1203cb5`)  
**Nota:** O subagente confundiu *rainhas reinantes* com *consortes de chefes de Estado*. O erro é de categoria: a dialética trata de mulheres soberanas no próprio direito, não de esposas de titulares de cargos republicanos. A síntese abaixo corrige o desvio.

---

## 1. Síntese do Conceito de *Feminilidade de Estado* (~500 palavras)

A *Feminilidade de Estado* designa a operação iconocrática que converte uma mulher em signo de soberania, tornando-a legível como tal enquanto apaga sua singularidade feminina. A antítese está plenamente certa no plano jurídico: no regime monárquico, o corpo da rainha não *representa* a soberania — ele a *encarna*. A doutrina dos *dois corpos do rei* (KANTOROWICZ, 1957/2016) demonstra que o corpo político é uma corporação *sole* — uma pessoa jurídica perpétua que nunca morre —, e o corpo natural do soberano é o seu instrumento *ex officio*, não seu signo alegórico. A iconografia monetária monárquica, portanto, não alegoriza a soberania; ela a *corporifica*. A efígie da rainha na moeda é a monarquia tornada visível, tangível, circulante.

Mas a tese sobrevive no plano iconográfico. Porque a Iconocracia não pergunta se a mulher *encarna* ou *representa* a soberania — ela pergunta o que acontece com a *mulher* quando ela entra no suporte estatal. E a resposta é a mesma em ambos os regimes: ela precisa deixar de ser mulher para ser signo de soberania. A República *fabrica* o corpo endurecido a partir do nada: Marianne não existe, é um corpo de pedra/gesso/metal que o Estado projeta como signo vazio. O endurecimento é *constitutivo* — a imagem só existe porque foi endurecida. A Monarquia, ao contrário, parte de um corpo real que *existe*, que envelhece, que tem biografia, maternidade, expressão. Para que esse corpo funcione como moeda, o Estado precisa *esvaziá-lo*: congelar a idade, apagar a expressão, neutralizar a sexualidade, reduzir a face a um perfil imutável. O endurecimento é *violento* — é uma alegorização *post mortem* em vida.

Essa operação não é meramente repressiva: ela é produtora de legibilidade. O Estado não só proíbe certas aparências — ele torna certos corpos legíveis como "boas" soberanas e outros como desviantes, impuros ou perigosos. A mesma gramática simbólica que organiza a iconografia monetária aparece em contextos muito distintos: a pureza maternal de Bharat Mata, a modéstia obrigatória no Irã, o véu e o burkini como alvos da soberania republicana francesa. A Iconocracia é um caso específico dessa gramática mais ampla: a mulher no suporte estatal é tornada legível como signo de soberania, mas essa legibilidade exige a eliminação de sua singularidade feminina.

Os casos scoutados confirmam a inversão. A Rainha Vitória no retrato "Old Head" (3ª efígie, 1895–1901) atinge score provisório 2.8/3: véu longo, diadema imperial, perfil congelado por seis anos enquanto a mulher envelhecia. Maria I nas moedas de 6400 Réis (ouro, 1789–1805) atinge 2.0/3: o véu de viúva funciona como marcador de luto que apaga maternidade e sexualidade. Elizabeth II na 5ª efígie (Jody Clark, 2015) atinge 1.7/3: o processo do RMAC exigiu um retrato "respeitoso" mas não idealizado, reconhecendo a idade sem a mostrar. O baseline do corpus (N=15 alegorias abstratas, score médio 2.1) revela o paradoxo: a Purificação Clássica atinge endurecimento comparável em corpos reais e fictícios. A República endurece o vazio; a Monarquia esvazia o corpo. Mas o resultado iconográfico é o mesmo: a mulher no suporte estatal deixa de ser *mulher* para ser *signo de soberania*.

A *Feminilidade de Estado*, portanto, ramifica-se em duas modalidades de endurecimento: o *constitutivo* (alegoria republicana) e o *violento* (corpo monárquico). A Iconocracia abrange as duas porque o *Contrato Sexual Visual* não distingue entre alegoria e pessoa — ele exige, em ambos os regimes, que a figura feminina no suporte estatal seja desprovida de sexo, de biografia, de tempo. A antítese está correta: juridicamente, representação e encarnação são categorias distintas. Iconograficamente, porém, ambas convergem para o mesmo ponto: a mulher como moeda. E essa convergência não é acidental: ela é a própria condição de legibilidade do símbolo estatal.

---

## 2. Proposta de Schema Delta para o Codebook v2

```yaml
# Campo novo a ser inserido em records.jsonl > purificacao
regime_iconografico:
  type: string
  enum: [republicano, monarquico, misto]
  description: >
    Regime iconográfico do suporte estatal. 'republicano' quando a figura feminina
    é uma alegoria abstrata (Marianne, Justiça, Liberdade). 'monarquico' quando
    a figura é uma mulher real e soberana (rainha reinante) em efígie oficial.
    'misto' quando há combinação de elementos alegóricos e corporais (ex: alegoria
    com atributos monárquicos, ou monarca em contexto alegórico).
  default: null
  validation: obrigatorio quando familia_alegorica = 'monarca-personificada'
```

**Nota:** Esta é uma hipótese de trabalho sujeita a validação com pelo menos 5 casos codificados em cada categoria antes de ser tornada obrigatória.

---

## 3. Matriz Comparativa: República vs. Monarquia

| Eixo | República (Endurecimento Constitutivo) | Monarquia (Endurecimento Violento) |
|------|----------------------------------------|------------------------------------|
| **Ponto de partida** | Mulher *não existe* (alegoria abstrata) | Mulher *existe* (soberana real) |
| **Mecanismo** | Fabrico do corpo endurecido a partir do vazio | Esvaziamento do corpo real até a efígie |
| **Endurecimento** | Constitutivo: a imagem só existe porque foi endurecida | Violento: o corpo é endurecido contra a sua própria biografia |
| **Tempo** | Atemporal (Marianne é sempre jovem, sempre igual) | Temporal (a rainha envelhece, mas a efígie congela) |
| **Juridicidade** | Representação: o signo *representa* a soberania | Encarnação: o signo *é* a soberania (king's two bodies) |
| **Iconografia** | Alegoria pura: corpo fabricado, sem referente biográfico | Efígie: corpo real reduzido a perfil imutável |
| **Exemplo corpus** | Marianne (score 2.4–3.0) | Vitória "Old Head" (score 2.8 provisório) |
| **Contrato Sexual Visual** | Exige que a mulher seja um signo vazio | Exige que a mulher deixe de ser mulher para ser moeda |

---

## 4. Nota sobre a Ausência da Categoria `monarca-personificada`

O codebook atual do corpus ICONOCRACIA não possui a categoria `monarca-personificada`. Das 328 entradas em `records.jsonl`, zero estão classificadas como tal. À primeira vista, isso parece uma lacuna metodológica. Mas, sob a ótica da *Purificação Clássica*, a ausência é **evidência**. O esquema de codificação tem categorias para alegorias abstratas — `Virtudes`, `Nacional`, `Continentes`, `Oceanos/Rios` — mas nenhum lugar para uma mulher real que governa. O codebook *vê* Marianne, Justiça, Liberdade, América. Ele não *vê* Victoria, Maria I, Elizabeth II. Essa cegueira não é acidental: ela reproduz exatamente a operação que a tese descreve. A Iconocracia transforma mulheres em ícones; o codebook, ao classificar apenas ícones, confirma que a categoria "mulher real soberana" foi eliminada do universo classificatório. A ausência da categoria `monarca-personificada` não é um bug — é a prova de que a Purificação Clássica funciona.

---

## Próximos Passos

1. **Revisão por Ana:** Avaliar se a síntese captura o movimento desejado. A antítese foi absorvida ou precisa de bridge paragraph mais explícito?
2. **Coding oficial:** submeter os 3 casos scoutados a `code_purification.py` para scores canônicos (não provisórios).
3. **Escolha de artefato:** subseção Cap.2, painel Atlas Cap.9, ou artigo curto — aguarda decisão de Ana.
4. **Schema delta:** validar `regime_iconografico` com pelo menos 5 casos em cada categoria antes de tornar obrigatório.
