"""Generate local review previews; never edits the ledger or publishes a site."""
import argparse
import html
import json
from pathlib import Path

try:
    from .publication_contract import real_url
except ImportError:
    from publication_contract import real_url

STYLE = 'body{max-width:850px;margin:3rem auto;padding:0 1rem;font:18px/1.6 system-ui;color:#252525}h1{line-height:1.2}a{color:#192675;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f3f6;padding:1rem}li{margin:.6rem 0}.status{border-left:5px solid #ac6600;padding:1rem;background:#fff5df}dt{font-weight:bold}dd{margin:0 0 1rem}small{overflow-wrap:anywhere}'


def read(path):
    return json.loads(path.read_text())


def page(title, body):
    return f'<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>{html.escape(title)}</title><style>{STYLE}</style><main>{body}</main></html>'


def build(audit, evidence_path, out):
    inventory = read(audit / 'inventory.json')
    pilot = read(audit / 'pilot.json')
    evidence = read(evidence_path)
    rows = {r['item_id']: r for r in inventory['records']}
    if len(pilot) != 12 or len({r['item_id'] for r in pilot}) != 12:
        raise ValueError('Pilot must contain 12 distinct records')
    out.mkdir(parents=True, exist_ok=True)
    links, packet = [], []
    for selection in pilot:
        rid = selection['item_id']
        row = rows[rid]
        review = evidence.get(rid, {'state': 'not_examined', 'blockers': ['Revisão documental e visual ainda não executada.']})
        label = ' / '.join(row['public_ids']) or rid
        esc = html.escape
        status = 'Revisão parcial — sem aprovação de publicação' if review['state'] != 'not_examined' else 'Não examinado — sem aprovação de publicação'
        body = f'<a href="index.html">← Piloto de revisão</a><h1>{esc(label)} · {esc(row["title"])}</h1><p class="status">{status}</p><small>UUID: {rid}</small>'
        url = row['source_url']
        if real_url(url):
            body += f'<p><a href="{esc(url, quote=True)}" rel="noreferrer">Fonte registrada no ledger</a> (não implica consulta concluída)</p>'
        else:
            body += '<p>Fonte registrada ausente ou provisória.</p>'
        if review.get('description'):
            body += f'<h2>Descrição observada, em revisão</h2><p>{esc(review["description"])}</p>'
        if review.get('interpretation'):
            body += f'<h2>Interpretação proposta</h2><p>{esc(review["interpretation"])}</p>'
        body += '<h2>Propostas por campo</h2>'
        for change in review.get('changes', []):
            body += '<pre>' + esc(json.dumps(change, ensure_ascii=False, indent=2)) + '</pre>'
        if not review.get('changes'):
            body += '<p>Nenhuma alteração evidenciada preparada nesta rodada.</p>'
        body += '<h2>Pendências</h2><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in review.get('blockers', [])) + '</ul>'
        body += '<details><summary>Auditoria técnica — não substitui revisão</summary><pre>' + esc(json.dumps(row,ensure_ascii=False,indent=2)) + '</pre></details>'
        (out / f'{rid}.html').write_text(page(label,body))
        links.append(f'<li><a href="{rid}.html">{esc(label)} — {esc(row["title"])}</a><br><small>{status}</small></li>')
        packet.append({'item_id':rid,'public_ids':row['public_ids'],'audit':row,'review':review})
    (out/'index.html').write_text(page('ICONOCRACIA — piloto de revisão','<h1>Piloto de 12 registros</h1><p class="status">Prévia local de trabalho. Nenhuma destas páginas é uma ficha pública aprovada.</p><p>Observação, interpretação e consulta documental permanecem separadas. Ausência de proposta não significa ausência de problema.</p><ol>'+''.join(links)+'</ol>'))
    (out/'review-packet.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    return packet


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit',type=Path,required=True)
    parser.add_argument('--evidence',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    packet=build(args.audit,args.evidence,args.out)
    print(f'{len(packet)} prévias; {sum(bool(r["review"].get("changes")) for r in packet)} casos com propostas; nenhuma promoção ao ledger.')
