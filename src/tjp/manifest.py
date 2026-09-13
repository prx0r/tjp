"""Dataset manifest format — every build produces one of these.

Provenance: commit + schemas + source snapshots + assumptions.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import datetime
import hashlib
import json


@dataclass
class DatasetManifest:
    dataset: str
    version: str
    generated_at: str  # ISO
    git_commit: str
    row_count: int
    schema_version: str
    raw_snapshot_hashes: List[str] = field(default_factory=list)
    strategies: List[str] = field(default_factory=list)
    feature_cutoff_policy: str = "point_in_time_v1"
    execution_assumptions: Optional[dict] = None
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "dataset": self.dataset,
            "version": self.version,
            "generated_at": self.generated_at,
            "git_commit": self.git_commit,
            "row_count": self.row_count,
            "schema_version": self.schema_version,
            "raw_snapshot_hashes": self.raw_snapshot_hashes,
            "strategies": self.strategies,
            "feature_cutoff_policy": self.feature_cutoff_policy,
            "execution_assumptions": self.execution_assumptions or {},
            "notes": self.notes,
        }

    def content_hash(self) -> str:
        return hashlib.sha256(json.dumps(self.to_dict(), sort_keys=True).encode()).hexdigest()[:16]


def make_manifest(
    dataset: str,
    version: str,
    git_commit: str,
    row_count: int,
    schema_version: str,
    strategies: List[str],
    execution_assumptions: Optional[dict] = None,
    notes: str = "",
) -> DatasetManifest:
    return DatasetManifest(
        dataset=dataset,
        version=version,
        generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        git_commit=git_commit,
        row_count=row_count,
        schema_version=schema_version,
        strategies=strategies,
        execution_assumptions=execution_assumptions,
        notes=notes,
    )
