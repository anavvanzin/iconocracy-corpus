#!/usr/bin/env python3
"""Fill missing suporte, motivo_alegorico, seculo fields in SCOUT-*.md files."""
import re, os, glob, sys

WORKDIR = os.path.dirname(os.path.abspath(__file__))

def get_files():
    files = sorted(glob.glob(os.path.join(WORKDIR, 'SCOUT-*.md')))
    # Exclude NC-, ZW-, SESSION-
    files = [f for f in files if not os.path.basename(f).startswith('SCOUT-NC-')
             and not os.path.basename(f).startswith('SCOUT-ZW-')
             and 'SESSION' not in os.path.basename(f)]
    return files

def parse_yaml(content):
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return None, None, content
    yaml_str = m.group(1)
    rest = content[m.end():]
    return yaml_str, m, rest

def has_field(yaml_str, field):
    return re.search(rf'^{field}:\s', yaml_str, re.MULTILINE) is not None

def extract_field(yaml_str, field):
    m = re.search(rf'^{field}:\s*(.*)', yaml_str, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None

def infer_suporte(title, url, body, yaml_str):
    """Infer suporte from title, URL, body content."""
    tlower = (title or '').lower()
    abnt = ''
    # Extract ABNT citation from body
    m = re.search(r'### Citação ABNT\n(.*?)(?:\n\n|\n###|\Z)', body, re.DOTALL)
    if m:
        abnt = m.group(1).lower()
    
    full_text = tlower + ' ' + abnt
    
    # Check title keywords first (most specific)
    # Moeda indicators
    coin_words = ['lire', 'mark', 'franc', 'peseta', 'cent', 'dollar', 'escudo',
                  'penny', 'reis', 'réis', 'reichsmark', 'reichspfennig', 'pfennig',
                  'halfpenny', 'florin', 'piastre', 'pesetas', 'francs', 'lire',
                  'réis', 'reis']
    for w in coin_words:
        if re.search(r'\b' + re.escape(w) + r'\b', tlower):
            return 'moeda'
    
    # Selo indicators
    stamp_words = ['selo', 'stamp', 'overprint', 'série ceres', 'semeuse']
    for w in stamp_words:
        if re.search(r'\b' + re.escape(w) + r'\b', tlower):
            return 'selo'
    
    # Papel-moeda indicators
    paper_words = ['banknote', 'assignat', 'cédula', 'cedula', 'silver certificate',
                   'reichsbanknote', 'notgeld', 'certificate', 'educational series']
    for w in paper_words:
        if re.search(r'\b' + re.escape(w) + r'\b', tlower):
            return 'papel-moeda'
    
    # Medalha
    if re.search(r'\bmedalha\b', tlower) or re.search(r'\bmedal\b', tlower):
        return 'medalha'
    
    # Check ABNT citation for medium clues
    if 'fotografia' in abnt or 'photograph' in abnt:
        return 'fotografia'
    if 'cartaz' in abnt or 'poster' in abnt:
        return 'cartaz'
    if 'pintura' in abnt or 'óleo' in abnt or 'oil on' in abnt:
        return 'pintura'
    if 'escultura' in abnt or 'sculpture' in abnt or 'fonte' in abnt or 'statue' in abnt:
        return 'escultura'
    if 'medalha' in abnt or 'medal' in abnt:
        return 'medalha'
    if 'gravura' in abnt or 'engraving' in abnt or 'etching' in abnt or 'print' in abnt:
        return 'estampa'
    if 'estampa' in abnt:
        return 'estampa'
    if 'desenho' in abnt or 'drawing' in abnt:
        return 'estampa'
    if 'litografia' in abnt or 'lithograph' in abnt:
        return 'estampa'
    if 'moeda' in abnt or 'coin' in abnt:
        return 'moeda'
    if 'selo' in abnt or 'stamp' in abnt:
        return 'selo'
    if 'cédula' in abnt or 'banknote' in abnt or 'papel-moeda' in abnt:
        return 'papel-moeda'
    
    # Check title for medium indicators
    if 'fotografia' in tlower or 'photograph' in tlower:
        return 'fotografia'
    if 'cartaz' in tlower or 'poster' in tlower:
        return 'cartaz'
    if 'pintura' in tlower or 'óleo' in tlower:
        return 'pintura'
    if 'escultura' in tlower or 'sculpture' in tlower or 'statue' in tlower or 'estátua' in tlower:
        return 'escultura'
    if 'monument' in tlower or 'temple' in tlower or 'altar' in tlower or 'palais' in tlower:
        return 'escultura'
    if 'fountain' in tlower or 'fonte' in tlower or 'brunnen' in tlower:
        return 'escultura'
    if 'gravura' in tlower or 'estampa' in tlower or 'estampe' in tlower:
        return 'estampa'
    if 'desenho' in tlower or 'drawing' in tlower or 'étude' in tlower:
        return 'estampa'
    if 'litografia' in tlower or 'lithograph' in tlower:
        return 'estampa'
    if 'caricature' in tlower or 'caricatura' in tlower:
        return 'estampa'
    if 'illustra' in tlower or 'illustrated' in tlower or 'ilustrada' in tlower:
        return 'estampa'
    if 'capa' in tlower or 'cover' in tlower or 'revista' in tlower:
        return 'estampa'
    if 'frontispicio' in tlower or 'frontispício' in tlower:
        return 'estampa'
    if 'pageant' in tlower:
        return 'fotografia'
    
    # Last resort: check "Motivos identificados" in body for clues
    m = re.search(r'\*\*Motivos identificados\*\*:\s*(.*)', body)
    if m:
        motivos = m.group(1).lower()
        if 'stamp' in motivos or 'selo' in motivos:
            return 'selo'
        if 'coin' in motivos or 'moeda' in motivos:
            return 'moeda'
        if 'banknote' in motivos or 'notgeld' in motivos:
            return 'papel-moeda'
    
    return None

def infer_motivo(title, body, yaml_str):
    """Infer motivo_alegorico from title and body."""
    tlower = (title or '').lower()
    
    # Extract Motivos identificados
    m = re.search(r'\*\*Motivos identificados\*\*:\s*(.*)', body)
    motivos = m.group(1).lower() if m else ''
    
    combined = tlower + ' ' + motivos
    
    # Priority order for figure types (most specific first)
    if re.search(r'\bjustiti?a\b', combined, re.IGNORECASE) or \
       re.search(r'\bjustice\b', combined, re.IGNORECASE) or \
       re.search(r'\bgerechtigkeit\b', combined, re.IGNORECASE) or \
       re.search(r'\brechtvaardigheid\b', combined, re.IGNORECASE) or \
       re.search(r'\bjustiça\b', combined, re.IGNORECASE) or \
       re.search(r'\biustitia\b', combined, re.IGNORECASE) or \
       re.search(r'\bjus civile\b', combined, re.IGNORECASE):
        return 'Justitia'
    
    if re.search(r'\bgermania\b', combined, re.IGNORECASE):
        return 'Germania'
    
    if re.search(r'\bbritannia\b', combined, re.IGNORECASE):
        return 'Britannia'
    
    if re.search(r'\bcolumbia\b', combined, re.IGNORECASE):
        return 'Columbia'
    
    if re.search(r'\bhispania\b', combined, re.IGNORECASE):
        return 'Hispania'
    
    if re.search(r'\bitalia turrita\b', combined, re.IGNORECASE):
        return 'Italia Turrita'
    
    if re.search(r'\bmarianne\b', combined, re.IGNORECASE):
        return 'Marianne'
    
    if re.search(r'\bla république\b', combined, re.IGNORECASE) or \
       re.search(r'\brépublique\b', combined, re.IGNORECASE) or \
       re.search(r'\brepublic\b', combined, re.IGNORECASE) or \
       re.search(r'\brepública\b', combined, re.IGNORECASE) or \
       re.search(r'\ba república\b', combined, re.IGNORECASE):
        # Distinguish La République vs generic
        if re.search(r'\bla république\b', combined, re.IGNORECASE) or \
           re.search(r'\brépublique\b', combined, re.IGNORECASE):
            return 'La République'
        if re.search(r'\ba república\b', combined, re.IGNORECASE) or \
           re.search(r'\brepública\b', combined, re.IGNORECASE):
            return 'A República'
        return 'Republic'
    
    if re.search(r'\blibert[éy]\b', combined, re.IGNORECASE) or \
       re.search(r'\bliberdade\b', combined, re.IGNORECASE):
        return 'Liberty'
    
    if re.search(r'\bsemeuse\b', combined, re.IGNORECASE) or \
       re.search(r'\bsemeadora\b', combined, re.IGNORECASE):
        return 'La Semeuse'
    
    if re.search(r'\bcérès\b', combined, re.IGNORECASE) or \
       re.search(r'\bceres\b', combined, re.IGNORECASE):
        return 'Cérès'
    
    if re.search(r'\bconstitution\b', combined, re.IGNORECASE):
        return 'Constitution'
    
    if re.search(r'\bpaix\b', combined, re.IGNORECASE) or \
       re.search(r'\bpeace\b', combined, re.IGNORECASE):
        return 'Peace'
    
    if re.search(r'\bempire\b', combined, re.IGNORECASE) or \
       re.search(r'\bempire\b', combined, re.IGNORECASE):
        return 'Empire'
    
    if re.search(r'\balegoria\b', combined, re.IGNORECASE) or \
       re.search(r'\ballegor', combined, re.IGNORECASE) or \
       re.search(r'\bfemale\b', combined, re.IGNORECASE):
        return 'Alegoria feminina'
    
    if re.search(r'\bpatria\b', combined, re.IGNORECASE) or \
       re.search(r'\bpátria\b', combined, re.IGNORECASE):
        return 'Pátria'
    
    if re.search(r'\bnotre-dame\b', combined, re.IGNORECASE):
        return 'Notre-Dame / La République'
    
    if re.search(r'\bmadame\b', combined, re.IGNORECASE):
        return 'Contra-alegoria'
    
    if re.search(r'\bfeminism', combined, re.IGNORECASE) or \
       re.search(r'\bsuffrag', combined, re.IGNORECASE):
        return 'Contra-alegoria'
    
    return None

def compute_seculo(data_estimada):
    """Compute seculo from data_estimada."""
    if not data_estimada or data_estimada.lower() in ('unknown', '', '""', "''"):
        return None
    
    de = data_estimada.strip().strip('"').strip("'")
    
    # Handle "Xth century" patterns
    m = re.match(r'(\d+)(?:st|nd|rd|th)\s+century', de, re.IGNORECASE)
    if m:
        return m.group(1) + 'th'
    
    m = re.match(r'early\s+(\d+)(?:st|nd|rd|th)\s+century', de, re.IGNORECASE)
    if m:
        return m.group(1) + 'th'
    
    # Extract first year-like number
    # Handle patterns like "c. 1560", "c. 1888 (final...)", "ca. 1917"
    # First, try to find a 4-digit year
    year_match = re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', de)
    if year_match:
        year = int(year_match.group(1))
        century = ((year - 1) // 100) + 1
        return str(century) + 'th'
    
    # Try 3-digit years (rare, like 800s)
    year_match = re.search(r'\b([5-9][0-9]{2}|1[0-2][0-9]{2})\b', de)
    if year_match:
        year = int(year_match.group(1))
        century = ((year - 1) // 100) + 1
        return str(century) + 'th'
    
    return None

def insert_field(yaml_str, field, value):
    """Insert a field into YAML frontmatter, placing it logically."""
    lines = yaml_str.split('\n')
    
    # Determine insertion point based on field
    if field == 'suporte':
        # Insert after 'data_scout:' line, or after 'records_item_id:'
        insert_after = ['records_item_id:', 'data_scout:']
        for i, line in enumerate(lines):
            for pat in insert_after:
                if line.strip().startswith(pat):
                    lines.insert(i + 1, f'{field}: {value}')
                    return '\n'.join(lines)
        # Fallback: end of yaml
        lines.append(f'{field}: {value}')
        return '\n'.join(lines)
    
    elif field == 'motivo_alegorico':
        # Insert after 'records_item_id:' or 'data_scout:'
        insert_after = ['records_item_id:', 'data_scout:']
        for i, line in enumerate(lines):
            for pat in insert_after:
                if line.strip().startswith(pat):
                    lines.insert(i + 1, f'{field}: {value}')
                    return '\n'.join(lines)
        lines.append(f'{field}: {value}')
        return '\n'.join(lines)
    
    elif field == 'seculo':
        # Insert near data_estimada or after motivo_alegorico
        insert_after = ['motivo_alegorico:', 'data_estimada:', 'records_item_id:']
        for i, line in enumerate(lines):
            for pat in insert_after:
                if line.strip().startswith(pat):
                    lines.insert(i + 1, f'{field}: {value}')
                    return '\n'.join(lines)
        lines.append(f'{field}: {value}')
        return '\n'.join(lines)
    
    return yaml_str

def main():
    files = get_files()
    print(f'Total files to check: {len(files)}')
    
    stats = {'suporte_filled': 0, 'motivo_filled': 0, 'seculo_filled': 0,
             'suporte_skipped': 0, 'motivo_skipped': 0, 'seculo_skipped': 0,
             'problematic': []}
    
    for filepath in files:
        fname = os.path.basename(filepath)
        with open(filepath, 'r') as f:
            content = f.read()
        
        yaml_str, yaml_match, rest = parse_yaml(content)
        if yaml_str is None:
            print(f'  NO YAML: {fname}')
            continue
        
        title = extract_field(yaml_str, 'titulo') or ''
        data_est = extract_field(yaml_str, 'data_estimada') or ''
        url = extract_field(yaml_str, 'url') or ''
        
        modified = False
        
        # Check suporte
        if not has_field(yaml_str, 'suporte'):
            suporte = infer_suporte(title, url, rest, yaml_str)
            if suporte:
                yaml_str = insert_field(yaml_str, 'suporte', suporte)
                stats['suporte_filled'] += 1
                modified = True
                print(f'  SUPORTE: {fname} -> {suporte}')
            else:
                stats['suporte_skipped'] += 1
                stats['problematic'].append(f'{fname}: could not infer suporte')
                print(f'  SUPORTE: {fname} -> COULD NOT INFER')
        
        # Check motivo_alegorico
        if not has_field(yaml_str, 'motivo_alegorico'):
            motivo = infer_motivo(title, rest, yaml_str)
            if motivo:
                yaml_str = insert_field(yaml_str, 'motivo_alegorico', motivo)
                stats['motivo_filled'] += 1
                modified = True
                print(f'  MOTIVO: {fname} -> {motivo}')
            else:
                stats['motivo_skipped'] += 1
                stats['problematic'].append(f'{fname}: could not infer motivo')
                print(f'  MOTIVO: {fname} -> COULD NOT INFER')
        
        # Check seculo
        if not has_field(yaml_str, 'seculo'):
            seculo = compute_seculo(data_est)
            if seculo:
                yaml_str = insert_field(yaml_str, 'seculo', seculo)
                stats['seculo_filled'] += 1
                modified = True
                print(f'  SECULO: {fname} -> {seculo}')
            else:
                stats['seculo_skipped'] += 1
                stats['problematic'].append(f'{fname}: could not compute seculo from "{data_est}"')
                print(f'  SECULO: {fname} -> COULD NOT COMPUTE (data={data_est})')
        
        if modified:
            new_content = '---\n' + yaml_str + '\n---' + rest
            with open(filepath, 'w') as f:
                f.write(new_content)
    
    print('\n=== SUMMARY ===')
    print(f'Suporte filled: {stats["suporte_filled"]}, skipped: {stats["suporte_skipped"]}')
    print(f'Motivo filled: {stats["motivo_filled"]}, skipped: {stats["motivo_skipped"]}')
    print(f'Seculo filled: {stats["seculo_filled"]}, skipped: {stats["seculo_skipped"]}')
    print(f'Total fields filled: {stats["suporte_filled"] + stats["motivo_filled"] + stats["seculo_filled"]}')
    
    if stats['problematic']:
        print(f'\n=== PROBLEMATIC FILES ({len(stats["problematic"])}) ===')
        for p in stats['problematic']:
            print(f'  {p}')

if __name__ == '__main__':
    main()
