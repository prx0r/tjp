from __future__ import annotations
import csv, yaml
from pathlib import Path
from .models import Scenario, Company


def load_config(path: str|Path):
    with open(path,"r",encoding="utf-8") as f: return yaml.safe_load(f)


def load_scenarios(path: str|Path) -> list[Scenario]:
    cfg=load_config(path)
    return [Scenario(**x) for x in cfg["scenarios"]]


def load_companies(path: str|Path) -> list[Company]:
    out=[]
    with open(path,newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            exp={k.removeprefix("exp_"):float(v) for k,v in r.items() if k.startswith("exp_") and v!=""}
            out.append(Company(
                ticker=r["ticker"],name=r["name"],sector=r["sector"],
                cashflow_duration=float(r["cashflow_duration"]),
                technological_duration=float(r["technological_duration"]),
                evidence_confidence=float(r.get("evidence_confidence",1)),
                exposures=exp,
            ))
    return out
