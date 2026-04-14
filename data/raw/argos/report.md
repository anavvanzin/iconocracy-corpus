# ARGOS acquisition report

## 1. Run metadata
- Manifest version: 1.0
- Generated at: 2026-04-14T03:37:40Z
- Storage root: /Volumes/ICONOCRACIA/corpus/imagens
- Storage tier: ssd
- Items covered: 20

## 2. Summary counts
- total_items: 20
- pending: 0
- success: 0
- partial: 0
- failed: 14
- manual: 6

## 3. Per-domain breakdown
| Domain | Items | Statuses |
| --- | ---: | --- |
| acervos.ims.com.br | 1 | failed=1 |
| archive.nyu.edu | 1 | failed=1 |
| be-monumen.be | 1 | failed=1 |
| brasiliana.museus.gov.br | 1 | failed=1 |
| brasilianafotografica.bn.gov.br | 4 | failed=4 |
| collections.heritage.brussels | 1 | failed=1 |
| colnect.com | 1 | manual=1 |
| eliseuvisconti.com.br | 1 | failed=1 |
| en.numista.com | 5 | manual=5 |
| en.wikipedia.org | 1 | failed=1 |
| memoria.bn.br | 2 | failed=2 |
| www.loc.gov | 1 | failed=1 |

## 4. Failure taxonomy
| Failure class | Count |
| --- | ---: |
| 404_not_found | 1 |
| iiif_image_unavailable | 1 |
| iiif_unavailable | 4 |
| manual_required | 6 |
| unexpected_content_type | 8 |

## 5. Manual-intervention checklist
- [ ] AR-001 | colnect.com | manual_required | Playwright fallback for colnect.com requires manual review unless explicitly allowed | Open the source URL in a logged-in browser, capture the canonical image, and record provenance notes. | https://colnect.com/en/stamps/stamp/128820-Allegory_Liberty_Seated-Allegory-Argentina
- [ ] BE-5F-LEOPOLD-1832 | en.numista.com | manual_required | Playwright fallback for numista.com requires manual review unless explicitly allowed | Open the source URL in a logged-in browser, capture the canonical image, and record provenance notes. | https://en.numista.com/catalogue/pieces255.html
- [ ] BE-CONGO-100F-1912 | en.numista.com | manual_required | Playwright fallback for numista.com requires manual review unless explicitly allowed | Open the source URL in a logged-in browser, capture the canonical image, and record provenance notes. | https://en.numista.com/258715
- [ ] BE-IND-1880 | en.numista.com | manual_required | Playwright fallback for numista.com requires manual review unless explicitly allowed | Open the source URL in a logged-in browser, capture the canonical image, and record provenance notes. | https://en.numista.com/catalogue/pieces27258.html
- [ ] BE-CONGO-1912 | en.numista.com | manual_required | Playwright fallback for numista.com requires manual review unless explicitly allowed | Open the source URL in a logged-in browser, capture the canonical image, and record provenance notes. | https://en.numista.com/catalogue/note258714.html
- [ ] BR-1000R-1906 | en.numista.com | manual_required | Playwright fallback for numista.com requires manual review unless explicitly allowed | Open the source URL in a logged-in browser, capture the canonical image, and record provenance notes. | https://en.numista.com/catalogue/pieces14484.html

## 6. Next-action suggestions
- Prioritize manual browser retrieval for blocked or policy-gated sources and log the operator workflow.
- Inspect content-type mismatches for HTML landing pages, redirects, or API responses before downloading again.
- Audit IIIF manifests and image-service URLs before retrying IIIF discovery or extraction.
- Re-check direct URLs returning 404/4xx responses; treat them as moved, withdrawn, or mistyped until confirmed otherwise.
