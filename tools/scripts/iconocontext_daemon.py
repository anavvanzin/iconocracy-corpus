#!/usr/bin/env python3
import http.server
import socketserver
import json
from pathlib import Path

PORT = 8080
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECORDS_FILE = REPO_ROOT / "data" / "processed" / "records.jsonl"

class IconoContextHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress console log spam

    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            try:
                metrics = self.calculate_metrics()
                self.wfile.write(json.dumps(metrics, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Error generating metrics: {str(e)}")
        else:
            self.send_response(404)
            self.end_headers()

    def calculate_metrics(self):
        records = []
        if RECORDS_FILE.exists():
            with open(RECORDS_FILE, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
                        
        total_records = len(records)
        recent = [r["purificacao"].get("id", "unk") for r in records[-5:] if "purificacao" in r]
        
        # Calculate indicator statistics
        indicators_sum = {}
        indicators_count = {}
        for r in records:
            purif = r.get("purificacao", {})
            for key, val in purif.items():
                if isinstance(val, int) and key != "purificacao_composto":
                    indicators_sum[key] = indicators_sum.get(key, 0) + val
                    indicators_count[key] = indicators_count.get(key, 0) + 1
                    
        means = {k: round(indicators_sum[k] / indicators_count[k], 2) for k in indicators_sum}
        
        return {
            "total_records": total_records,
            "recent_records": recent,
            "purification_means": means,
            "daemon_status": "healthy"
        }

def run_daemon():
    # Allow port reuse to avoid 'Address already in use' errors
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), IconoContextHandler) as httpd:
        print(f"IconoContext Daemon running on port {PORT}...")
        httpd.serve_forever()

if __name__ == "__main__":
    run_daemon()
