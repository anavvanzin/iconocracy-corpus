#!/usr/bin/env python3
"""
ICONOCRACY Gallica Discovery Pipeline
Uses mcporter to systematically search Gallica for female allegorical figures.
"""

import json
import subprocess
import sys
from pathlib import Path
import time

class GallicaDiscovery:
    def __init__(self):
        self.gallica_server_path = Path(__file__).parent.parent.parent / "indexing" / "gallica-mcp-server"
        self.output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
        
        # ICONOCRACY search terms optimized for French archives
        self.search_strategies = [
            {
                "name": "republican_allegories", 
                "terms": ["République française", "allégorie République", "Marianne"],
                "supports": ["image"]
            },
            {
                "name": "justice_figures",
                "terms": ["Justice", "Justitia", "balance justice"],
                "supports": ["image"]
            },
            {
                "name": "liberty_figures", 
                "terms": ["Liberté", "allégorie liberté", "figure liberté"],
                "supports": ["image"]
            },
            {
                "name": "medals_coins",
                "terms": ["médaille République", "monnaie République", "frappe médaille"],
                "supports": ["image"]
            },
            {
                "name": "architecture_forensic",
                "terms": ["palais justice", "tribunal", "architecture judiciaire"],
                "supports": ["image"]
            },
            {
                "name": "stamps_prints",
                "terms": ["timbre République", "estampe République", "gravure allégorie"],
                "supports": ["image"]
            }
        ]

    def search_gallica(self, query, document_type="image", limit=20, date_from=None, date_to=None):
        """Execute Gallica search via mcporter"""
        cmd = [
            "npx", "mcporter", "call", 
            "--stdio", "node dist/index.js", 
            "gallica_search",
            "--args", json.dumps({
                "query": query,
                "document_type": document_type,
                "limit": limit,
                "date_from": date_from,
                "date_to": date_to,
                "response_format": "json"
            }),
            "--output", "json"
        ]
        
        try:
            result = subprocess.run(cmd, cwd=self.gallica_server_path, 
                                  capture_output=True, text=True, timeout=60)
            return json.loads(result.stdout) if result.returncode == 0 else None
        except Exception as e:
            print(f"Error searching '{query}': {e}")
            return None

    def iconographic_search(self, subject_terms, date_from=None, date_to=None, limit=15):
        """Use specialized iconographic search"""
        cmd = [
            "npx", "mcporter", "call",
            "--stdio", "node dist/index.js",
            "gallica_search_iconography", 
            "--args", json.dumps({
                "subject_terms": subject_terms,
                "date_from": date_from,
                "date_to": date_to,
                "limit": limit,
                "response_format": "json"
            }),
            "--output", "json"
        ]
        
        try:
            result = subprocess.run(cmd, cwd=self.gallica_server_path,
                                  capture_output=True, text=True, timeout=60)
            return json.loads(result.stdout) if result.returncode == 0 else None
        except Exception as e:
            print(f"Error in iconographic search {subject_terms}: {e}")
            return None

    def discover_candidates(self, period_focus="1880-1920", limit_per_search=25):
        """
        Execute systematic discovery for ICONOCRACY corpus candidates.
        
        Args:
            period_focus: Date range as "YYYY-YYYY" (priority period)  
            limit_per_search: Max results per individual search
        """
        date_from, date_to = period_focus.split("-")
        all_discoveries = []
        
        print(f"🔍 Starting Gallica discovery for period {period_focus}")
        print(f"📁 Server path: {self.gallica_server_path}")
        
        for strategy in self.search_strategies:
            print(f"\\n=== {strategy['name'].upper()} ===")
            
            for term in strategy["terms"]:
                print(f"  Searching: {term}")
                
                # Try regular search first
                results = self.search_gallica(
                    query=term,
                    document_type="image", 
                    limit=limit_per_search,
                    date_from=date_from,
                    date_to=date_to
                )
                
                if results and results.get("total", 0) > 0:
                    print(f"    📊 Found {results['total']} total, showing {results['count']}")
                    
                    # Filter for potential iconocracy candidates
                    for record in results.get("records", []):
                        candidate = self.assess_iconocracy_candidate(record, term, strategy['name'])
                        if candidate:
                            all_discoveries.append(candidate)
                else:
                    print(f"    ❌ No results")
                
                # Rate limiting
                time.sleep(1)
        
        return all_discoveries

    def assess_iconocracy_candidate(self, record, search_term, strategy):
        """
        Assess if a Gallica record matches ICONOCRACY inclusion criteria:
        - Female allegorical figure
        - Explicit juridical-political function  
        - Datable 1800-2000
        - Accepted country (here: France)
        - Accepted support
        """
        
        # Basic metadata extraction
        title = record.get("title", "").lower()
        subjects = [s.lower() for s in record.get("subject", [])]
        date = record.get("date", "")
        creator = record.get("creator", [])
        
        # Quick heuristic filtering 
        allegorical_indicators = [
            "république", "marianne", "liberté", "justice", "justitia", 
            "allégorie", "personnification", "figure"
        ]
        
        juridical_indicators = [
            "justice", "tribunal", "palais", "république", "état", 
            "droit", "loi", "constitution"
        ]
        
        # Check for allegorical + juridical elements
        has_allegory = any(ind in title or any(ind in s for s in subjects) 
                          for ind in allegorical_indicators)
        has_juridical = any(ind in title or any(ind in s for s in subjects)
                           for ind in juridical_indicators)
        
        if has_allegory and has_juridical:
            return {
                "ark": record.get("ark"),
                "url": record.get("url"), 
                "title": record.get("title"),
                "date": date,
                "creator": creator,
                "subjects": record.get("subject", []),
                "rights": record.get("rights"),
                "search_term": search_term,
                "strategy": strategy,
                "assessment": "potential_candidate",
                "format": record.get("format", ""),
                "iconocracy_score": self.score_candidate(record)
            }
        
        return None

    def score_candidate(self, record):
        """Basic scoring for prioritization (0-1 scale)"""
        score = 0.0
        
        title = record.get("title", "").lower()
        subjects = [s.lower() for s in record.get("subject", [])]
        
        # Bonus for key terms
        if any(term in title for term in ["marianne", "république", "justice"]):
            score += 0.3
        if any("allégorie" in s for s in subjects):
            score += 0.2
        if "domaine public" in record.get("rights", ""):
            score += 0.2
        if record.get("date"):
            try:
                year = int(record.get("date", "0"))
                if 1880 <= year <= 1920:  # Priority period
                    score += 0.3
                elif 1800 <= year <= 2000:  # Acceptable period
                    score += 0.1
            except:
                pass
        
        return min(score, 1.0)

    def save_discoveries(self, discoveries, filename="gallica_discoveries.json"):
        """Save discoveries to raw data directory"""
        output_file = self.output_dir / filename
        
        # Sort by iconocracy score
        discoveries.sort(key=lambda x: x.get("iconocracy_score", 0), reverse=True)
        
        discovery_report = {
            "discovery_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_candidates": len(discoveries),
            "high_priority": len([d for d in discoveries if d.get("iconocracy_score", 0) > 0.7]),
            "medium_priority": len([d for d in discoveries if 0.4 <= d.get("iconocracy_score", 0) <= 0.7]),
            "discoveries": discoveries
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(discovery_report, f, indent=2, ensure_ascii=False)
        
        print(f"\\n📄 Saved {len(discoveries)} discoveries to {output_file}")
        return output_file

def main():
    """Main discovery pipeline"""
    if len(sys.argv) > 1:
        period = sys.argv[1]
    else:
        period = "1880-1920"  # Default priority period for iconocracy
    
    discovery = GallicaDiscovery()
    candidates = discovery.discover_candidates(period_focus=period)
    
    if candidates:
        report_file = discovery.save_discoveries(candidates)
        
        print(f"\\n🎯 DISCOVERY SUMMARY")
        print(f"   Total candidates: {len(candidates)}")
        print(f"   High priority: {len([c for c in candidates if c.get('iconocracy_score', 0) > 0.7])}")
        print(f"   Report saved: {report_file}")
        
        # Show top 3 candidates
        print(f"\\n🏆 TOP CANDIDATES:")
        for i, candidate in enumerate(candidates[:3], 1):
            print(f"   {i}. {candidate['title']} (score: {candidate.get('iconocracy_score', 0):.2f})")
            print(f"      ARK: {candidate['ark']}")
            print(f"      Date: {candidate['date']}")
    else:
        print("\\n❌ No suitable candidates found")

if __name__ == "__main__":
    main()