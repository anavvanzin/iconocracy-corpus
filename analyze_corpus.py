#!/usr/bin/env python3
"""
ICONOCRACY Corpus Analysis Script
Analyzes the structure and distribution patterns in records.jsonl
"""
import json
from collections import defaultdict, Counter
from datetime import datetime
import re

def load_records(file_path):
    """Load JSONL records with error handling"""
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError as e:
                    print(f"Error parsing line {line_num}: {e}")
    return records

def extract_country_info(record):
    """Extract country information from various fields"""
    country_indicators = []
    
    # Check place_hint
    place_hint = record.get('input', {}).get('place_hint', '')
    if place_hint:
        country_indicators.append(place_hint)
    
    # Check URL patterns for country
    url = record.get('input', {}).get('input_url', '')
    if 'brasiliana' in url or '.br' in url:
        country_indicators.append('Brazil')
    elif '.fr' in url or 'gallica' in url:
        country_indicators.append('France')
    elif '.de' in url:
        country_indicators.append('Germany')
    elif '.it' in url:
        country_indicators.append('Italy')
    elif '.es' in url:
        country_indicators.append('Spain')
    
    # Check title and evidence for country hints
    title = record.get('input', {}).get('title_hint', '')
    evidence = record.get('webscout', {}).get('summary_evidence', '')
    
    combined_text = f"{title} {evidence}".lower()
    
    if any(word in combined_text for word in ['brazil', 'brasil', 'rio', 'são paulo', 'belém']):
        country_indicators.append('Brazil')
    elif any(word in combined_text for word in ['france', 'paris', 'marianne']):
        country_indicators.append('France')
    elif any(word in combined_text for word in ['germany', 'deutschland', 'germania']):
        country_indicators.append('Germany')
    elif any(word in combined_text for word in ['italy', 'italia', 'roma']):
        country_indicators.append('Italy')
    elif any(word in combined_text for word in ['spain', 'españa']):
        country_indicators.append('Spain')
    
    # Return most frequent indicator or 'Unknown'
    if country_indicators:
        return Counter(country_indicators).most_common(1)[0][0]
    return 'Unknown'

def extract_regime_info(record):
    """Extract regime classification from iconocode interpretation"""
    interpretations = record.get('iconocode', {}).get('interpretation', [])
    
    for interp in interpretations:
        claim_text = interp.get('claim_text', '')
        if 'Regime iconocrático:' in claim_text:
            # Extract regime type
            regime_match = re.search(r'Regime iconocrático:\s*([\w-]+)', claim_text)
            if regime_match:
                return regime_match.group(1).upper()
    
    return 'Unknown'

def extract_date_info(record):
    """Extract and normalize date information"""
    date_hint = record.get('input', {}).get('date_hint', '')
    if not date_hint:
        return None
    
    # Extract year from various formats
    year_match = re.search(r'(\d{4})', date_hint)
    if year_match:
        return int(year_match.group(1))
    
    return None

def analyze_iconclass_codes(record):
    """Extract iconclass codes and their frequencies"""
    codes = record.get('iconocode', {}).get('codes', [])
    iconclass_codes = []
    
    for code in codes:
        if code.get('scheme') == 'iconclass':
            notation = code.get('notation', '')
            if notation:
                iconclass_codes.append(notation)
    
    return iconclass_codes

def main():
    print("ICONOCRACY Corpus Structure Analysis")
    print("=" * 50)
    
    # Load records
    records_path = "data/processed/records.jsonl"
    records = load_records(records_path)
    
    print(f"\nTotal Records: {len(records)}")
    print(f"File: {records_path}")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize counters
    country_stats = Counter()
    regime_stats = Counter()
    date_stats = Counter()
    iconclass_stats = Counter()
    batch_stats = Counter()
    
    # Process each record
    detailed_analysis = []
    
    for record in records:
        item_id = record.get('item_id', 'unknown')
        batch_id = record.get('batch_id', 'unknown')
        
        # Extract information
        country = extract_country_info(record)
        regime = extract_regime_info(record)
        year = extract_date_info(record)
        iconclass_codes = analyze_iconclass_codes(record)
        
        # Update counters
        country_stats[country] += 1
        regime_stats[regime] += 1
        batch_stats[batch_id] += 1
        
        if year:
            decade = (year // 10) * 10
            date_stats[f"{decade}s"] += 1
        
        for code in iconclass_codes:
            iconclass_stats[code] += 1
        
        # Store detailed info
        detailed_analysis.append({
            'item_id': item_id,
            'country': country,
            'regime': regime,
            'year': year,
            'iconclass_codes': iconclass_codes,
            'title': record.get('input', {}).get('title_hint', ''),
            'batch_id': batch_id
        })
    
    # Print analysis results
    print("\n" + "="*50)
    print("DISTRIBUTION BY COUNTRY")
    print("="*50)
    for country, count in country_stats.most_common():
        percentage = (count / len(records)) * 100
        print(f"{country:15}: {count:3d} records ({percentage:5.1f}%)")
    
    print("\n" + "="*50)
    print("DISTRIBUTION BY REGIME")
    print("="*50)
    for regime, count in regime_stats.most_common():
        percentage = (count / len(records)) * 100
        print(f"{regime:15}: {count:3d} records ({percentage:5.1f}%)")
    
    print("\n" + "="*50)
    print("DISTRIBUTION BY DECADE")
    print("="*50)
    for decade, count in sorted(date_stats.items()):
        percentage = (count / len(records)) * 100
        print(f"{decade:15}: {count:3d} records ({percentage:5.1f}%)")
    
    print("\n" + "="*50)
    print("TOP ICONCLASS CODES")
    print("="*50)
    for code, count in iconclass_stats.most_common(15):
        percentage = (count / len(records)) * 100
        print(f"{code:15}: {count:3d} occurrences ({percentage:5.1f}%)")
    
    print("\n" + "="*50)
    print("BATCH DISTRIBUTION")
    print("="*50)
    for batch, count in batch_stats.most_common():
        percentage = (count / len(records)) * 100
        batch_short = batch[-12:] if len(batch) > 12 else batch
        print(f"{batch_short}: {count:3d} records ({percentage:5.1f}%)")
    
    # Cross-analysis: Country vs Regime
    print("\n" + "="*50)
    print("COUNTRY vs REGIME CROSS-ANALYSIS")
    print("="*50)
    
    country_regime_matrix = defaultdict(lambda: defaultdict(int))
    for item in detailed_analysis:
        country_regime_matrix[item['country']][item['regime']] += 1
    
    # Print matrix
    all_regimes = sorted(set(item['regime'] for item in detailed_analysis))
    print(f"{'Country':<15}", end="")
    for regime in all_regimes:
        print(f"{regime:>12}", end="")
    print(f"{'Total':>8}")
    print("-" * (15 + 12 * len(all_regimes) + 8))
    
    for country in sorted(country_regime_matrix.keys()):
        print(f"{country:<15}", end="")
        row_total = 0
        for regime in all_regimes:
            count = country_regime_matrix[country][regime]
            print(f"{count:>12}", end="")
            row_total += count
        print(f"{row_total:>8}")
    
    # Key findings summary
    print("\n" + "="*50)
    print("KEY FINDINGS")
    print("="*50)
    
    total_records = len(records)
    dominant_country = country_stats.most_common(1)[0] if country_stats else None
    dominant_regime = regime_stats.most_common(1)[0] if regime_stats else None
    most_common_code = iconclass_stats.most_common(1)[0] if iconclass_stats else None
    
    if dominant_country:
        print(f"• Dominant country: {dominant_country[0]} ({dominant_country[1]} records, {(dominant_country[1]/total_records)*100:.1f}%)")
    
    if dominant_regime:
        print(f"• Dominant regime: {dominant_regime[0]} ({dominant_regime[1]} records, {(dominant_regime[1]/total_records)*100:.1f}%)")
    
    if most_common_code:
        print(f"• Most frequent Iconclass code: {most_common_code[0]} ({most_common_code[1]} occurrences)")
    
    # Calculate temporal span
    years = [item['year'] for item in detailed_analysis if item['year']]
    if years:
        print(f"• Temporal span: {min(years)} - {max(years)} ({max(years) - min(years)} years)")
    
    # Calculate diversity metrics
    print(f"• Geographic diversity: {len(country_stats)} countries/regions")
    print(f"• Regime diversity: {len(regime_stats)} regime types")
    print(f"• Iconographic diversity: {len(iconclass_stats)} unique Iconclass codes")
    
    # Check for 48C51 (feminist iconography)
    feminist_count = iconclass_stats.get('48C51', 0)
    if feminist_count > 0:
        print(f"• Feminist iconography (48C51): {feminist_count} occurrences ({(feminist_count/total_records)*100:.1f}%)")
    
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()