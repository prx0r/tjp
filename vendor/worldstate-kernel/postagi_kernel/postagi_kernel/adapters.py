"""Production data adapter contracts.

Adapters return normalized records with explicit `asof` timestamps so the same
pipeline can be used live and in point-in-time backtests.
"""
from __future__ import annotations
from typing import Protocol, Iterable

class DocumentSource(Protocol):
    def iter_documents(self,start:str,end:str) -> Iterable[dict]: ...
class PatentSource(Protocol):
    def iter_patents(self,start:str,end:str) -> Iterable[dict]: ...
    def iter_citations(self,start:str,end:str) -> Iterable[dict]: ...
class MarketSource(Protocol):
    def prices(self,tickers:list[str],start:str,end:str) -> list[dict]: ...
    def fundamentals(self,tickers:list[str],asof:str) -> list[dict]: ...
class SupplyChainSource(Protocol):
    def transactions(self,start:str,end:str) -> Iterable[dict]: ...

RECOMMENDED_SOURCES={
  "papers":["arXiv","Crossref/OpenAlex"],
  "patents":["USPTO PatentsView","Google Patents public datasets"],
  "world_events":["GDELT/MIRAI"],
  "company_filings":["SEC EDGAR"],
  "supply_chain":["BACI/UN Comtrade","company disclosures","custom supplier graph"],
  "market":["CRSP/Compustat for research","licensed/live price provider for deployment"],
}
