"""SQLite event/evidence store for continuously updating world state."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path

SCHEMA='''
CREATE TABLE IF NOT EXISTS evidence(
 id TEXT PRIMARY KEY, ts TEXT NOT NULL, source_type TEXT NOT NULL,
 scenario_id TEXT NOT NULL, log_lr REAL NOT NULL, reliability REAL NOT NULL,
 payload_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_evidence_scenario_ts ON evidence(scenario_id,ts);
CREATE TABLE IF NOT EXISTS snapshots(
 ts TEXT NOT NULL, scenario_id TEXT NOT NULL, our_probability REAL NOT NULL,
 market_probability REAL NOT NULL, PRIMARY KEY(ts,scenario_id)
);
'''

class KernelStore:
    def __init__(self,path:str|Path):
        self.path=str(path); self.db=sqlite3.connect(self.path); self.db.executescript(SCHEMA)
    def add_evidence(self,e):
        self.db.execute('INSERT OR REPLACE INTO evidence VALUES(?,?,?,?,?,?,?)',
            (e.id,e.timestamp,e.source_type,e.target_scenario,e.log_likelihood_ratio,e.reliability,json.dumps(e.description)))
        self.db.commit()
    def evidence_for(self,scenario_id:str):
        rows=self.db.execute('SELECT id,ts,source_type,scenario_id,log_lr,reliability,payload_json FROM evidence WHERE scenario_id=? ORDER BY ts',(scenario_id,)).fetchall()
        return rows
    def close(self): self.db.close()
