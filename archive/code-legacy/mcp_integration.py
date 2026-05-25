#!/usr/bin/env python3
"""
MCP Integration for ICONOCRACY Research Pipeline

Provides Python wrapper functions for mcporter calls, integrating with existing 
dual-agent pipeline (WebScout → IconoCode). Designed to complement existing 
validation, sync, and purification scripts.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

class ICONOCRACYMCPClient:
    """
    MCP client for ICONOCRACY research operations.
    Integrates with existing corpus pipeline: WebScout → IconoCode → validation
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.gallica_server = self.base_path / "indexing" / "gallica-mcp-server"
        self.memory_server = "npx -y @modelcontextprotocol/server-memory"
        
        # Validate Gallica MCP server is available
        if not (self.gallica_server / "dist" / "index.js").exists():
            print("⚠️  Gallica MCP server not built. Run: cd indexing/gallica-mcp-server && npm run build")

    def gallica_search(self, query: str, **kwargs) -> Optional[Dict]:
        """
        Search Gallica archive via MCP.
        
        Args:
            query: Search term (free text or CQL)
            **kwargs: document_type, date_from, date_to, limit, field, etc.
        
        Returns:
            JSON response with results or None if error
        """
        args = {"query": query, "response_format": "json"}
        args.update(kwargs)
        
        return self._call_gallica("gallica_search", args)

    def gallica_iconographic_search(self, subject_terms: List[str], **kwargs) -> Optional[Dict]:
        """
        Specialized iconographic search using LPAI vocabulary.
        Ideal for allegorical figures.
        
        Args:
            subject_terms: List of LPAI terms like ["allégorie", "Justitia"]
            **kwargs: free_text, date_from, date_to, etc.
        """
        args = {"subject_terms": subject_terms, "response_format": "json"}
        args.update(kwargs)
        
        return self._call_gallica("gallica_search_iconography", args)

    def gallica_get_metadata(self, ark: str) -> Optional[Dict]:
        """Get full metadata for a Gallica item, including rights info"""
        return self._call_gallica("gallica_get_metadata", {
            "ark": ark, 
            "response_format": "json"
        })

    def gallica_get_image_url(self, ark: str, **kwargs) -> Optional[Dict]:
        """
        Generate high-res IIIF image URL.
        
        Args:
            ark: Document identifier
            **kwargs: page, region, size, format, fetch_info
        """
        args = {"ark": ark, "response_format": "json"}
        args.update(kwargs)
        
        return self._call_gallica("gallica_get_image_url", args)

    def _call_gallica(self, tool: str, args: Dict) -> Optional[Dict]:
        """Internal method to call Gallica MCP tools"""
        cmd = [
            "npx", "mcporter", "call",
            "--stdio", "node dist/index.js",
            tool,
            "--args", json.dumps(args),
            "--output", "json"
        ]
        
        try:
            result = subprocess.run(cmd, cwd=self.gallica_server,
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"Gallica error: {result.stderr}")
                return None
        except Exception as e:
            print(f"MCP call error: {e}")
            return None

    def memory_create_entity(self, name: str, entity_type: str, observations: List[str]) -> bool:
        """Create entity in knowledge graph"""
        return self._call_memory("create_entities", {
            "entities": [{
                "name": name,
                "entityType": entity_type, 
                "observations": observations
            }]
        })

    def memory_search(self, query: str) -> Optional[Dict]:
        """Search knowledge graph"""
        result = self._call_memory("search_nodes", {"query": query})
        return result

    def memory_read_graph(self) -> Optional[Dict]:
        """Get complete knowledge graph"""
        return self._call_memory("read_graph", {})

    def _call_memory(self, tool: str, args: Dict) -> Optional[Dict]:
        """Internal method to call memory MCP tools"""
        cmd = [
            "npx", "mcporter", "call", 
            "--stdio", self.memory_server,
            tool,
            "--args", json.dumps(args),
            "--output", "json"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"Memory error: {result.stderr}")
                return None
        except Exception as e:
            print(f"Memory call error: {e}")
            return None

    def webscout_gallica_enhancement(self, existing_record: Dict) -> Dict:
        """
        Enhance existing WebScout record with additional Gallica metadata.
        
        Compatible with master-record schema from tools/schemas/master-record.schema.json
        """
        enhanced_record = existing_record.copy()
        
        # Extract search hints from existing record
        input_data = existing_record.get("input", {})
        title_hint = input_data.get("title_hint", "")
        
        if not title_hint:
            return enhanced_record
        
        # Search for related items in Gallica
        search_results = self.gallica_search(title_hint, limit=5)
        
        if search_results and search_results.get("records"):
            # Add Gallica cross-references to webscout section
            webscout_section = enhanced_record.setdefault("webscout", {})
            gallica_refs = []
            
            for record in search_results["records"][:3]:  # Top 3 matches
                gallica_refs.append({
                    "evidence_id": f"gallica_{len(gallica_refs) + 1}",
                    "source_type": "cross_reference",
                    "title": record.get("title", ""),
                    "url": record.get("url", ""),
                    "ark": record.get("ark", ""),
                    "date": record.get("date", ""),
                    "rights": record.get("rights", ""),
                    "notes": f"Gallica cross-ref via MCP search: {title_hint}"
                })
            
            if gallica_refs:
                webscout_section["gallica_cross_refs"] = gallica_refs
                print(f"✅ Enhanced record {existing_record.get('item_id', 'unknown')} with {len(gallica_refs)} Gallica cross-references")
        
        return enhanced_record

    def batch_enhance_corpus(self, records_file: Path) -> int:
        """
        Enhance entire corpus with Gallica cross-references.
        
        Args:
            records_file: Path to records.jsonl
            
        Returns:
            Number of records enhanced
        """
        if not records_file.exists():
            print(f"❌ Records file not found: {records_file}")
            return 0
        
        enhanced_count = 0
        enhanced_records = []
        
        print(f"🔍 Enhancing corpus with Gallica cross-references...")
        
        with open(records_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    record = json.loads(line.strip())
                    enhanced = self.webscout_gallica_enhancement(record)
                    
                    # Check if actually enhanced
                    if "gallica_cross_refs" in enhanced.get("webscout", {}):
                        enhanced_count += 1
                    
                    enhanced_records.append(enhanced)
                    
                    if line_num % 10 == 0:
                        print(f"  Processed {line_num} records...")
                        
                except json.JSONDecodeError:
                    print(f"⚠️  Skipping malformed JSON at line {line_num}")
                    continue
                except Exception as e:
                    print(f"⚠️  Error processing record {line_num}: {e}")
                    continue
        
        # Write enhanced corpus
        enhanced_file = records_file.parent / "records_enhanced.jsonl"
        with open(enhanced_file, 'w', encoding='utf-8') as f:
            for record in enhanced_records:
                f.write(json.dumps(record, ensure_ascii=False) + '\\n')
        
        print(f"✅ Enhanced {enhanced_count} records out of {len(enhanced_records)}")
        print(f"📄 Saved to: {enhanced_file}")
        
        return enhanced_count


def main():
    """CLI interface for MCP operations"""
    
    if len(sys.argv) < 2:
        print("""
ICONOCRACY MCP Integration

Usage:
    python3 mcp_integration.py search "République française" 
    python3 mcp_integration.py iconographic "allégorie,Justitia"
    python3 mcp_integration.py enhance-corpus
    python3 mcp_integration.py memory-search "research"
    python3 mcp_integration.py metadata ark:/12148/btv1b530136230
        """)
        return

    mcp = ICONOCRACYMCPClient()
    command = sys.argv[1]

    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else "République française"
        results = mcp.gallica_search(query, limit=5)
        if results:
            print(f"Found {results.get('total', 0)} total results")
            for i, record in enumerate(results.get('records', []), 1):
                print(f"{i}. {record.get('title', 'No title')}")
                print(f"   ARK: {record.get('ark')}")
                print(f"   Date: {record.get('date', 'Unknown')}")
                print(f"   Rights: {record.get('rights', 'Unknown')}")

    elif command == "iconographic":
        terms = sys.argv[2].split(",") if len(sys.argv) > 2 else ["allégorie"]
        results = mcp.gallica_iconographic_search(terms, limit=5)
        if results and results.get('total', 0) > 0:
            print(f"Iconographic search found {results['total']} results")
            for record in results.get('records', []):
                print(f"- {record.get('title')}")
        else:
            print("No iconographic results found")

    elif command == "enhance-corpus":
        corpus_file = Path("data/processed/records.jsonl")
        enhanced = mcp.batch_enhance_corpus(corpus_file)
        print(f"Enhanced {enhanced} corpus records")

    elif command == "memory-search":
        query = sys.argv[2] if len(sys.argv) > 2 else "research"
        results = mcp.memory_search(query)
        if results:
            entities = results.get('entities', [])
            print(f"Memory search found {len(entities)} entities:")
            for entity in entities:
                print(f"- {entity['name']} ({entity['entityType']})")

    elif command == "metadata":
        ark = sys.argv[2] if len(sys.argv) > 2 else "ark:/12148/btv1b530136230"
        metadata = mcp.gallica_get_metadata(ark)
        if metadata:
            print(f"Title: {metadata.get('title', 'Unknown')}")
            print(f"Creator: {metadata.get('creator', [])}")
            print(f"Date: {metadata.get('date', 'Unknown')}")
            print(f"Rights: {metadata.get('rights', 'Unknown')}")

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()