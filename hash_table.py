"""
hash_table.py
-------------
Hash table implementation for a music application's Song ID index.

Hash function : Division Method      h(k) = k mod m
Collision handling : Separate Chaining (each bucket is a Python list)

Every public operation counts the primitive comparisons it performs so
that Part (b) and Part (c) of the assignment can report real, measured
numbers instead of guesses.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SearchResult:
    key: int
    found: bool
    comparisons: int          # key-comparisons performed inside the bucket
    bucket_index: Optional[int] = None
    probe_sequence: List[int] = field(default_factory=list)


class DivisionHashTable:
    def __init__(self, table_size: int):
        self.m = table_size
        self.table: List[List[int]] = [[] for _ in range(table_size)]
        self.insert_log: List[str] = []   # human-readable trace of every insert

    # ---------- hash function -------------------------------------------
    def h(self, key: int) -> int:
        return key % self.m

    # ---------- insert -----------------------------------------------------
    def insert(self, key: int) -> int:
        idx = self.h(key)
        bucket = self.table[idx]
        collided = len(bucket) > 0
        bucket.append(key)
        note = (f"insert({key}): h({key}) = {key} mod {self.m} = {idx}  "
                f"-> bucket[{idx}] = {bucket}"
                + ("   <-- COLLISION (bucket already occupied)" if collided else ""))
        self.insert_log.append(note)
        return idx

    def build(self, keys: List[int]) -> None:
        for k in keys:
            self.insert(k)

    # ---------- search -------------------------------------------------
    def search(self, key: int) -> SearchResult:
        idx = self.h(key)
        bucket = self.table[idx]
        comparisons = 0
        for item in bucket:
            comparisons += 1
            if item == key:
                return SearchResult(key, True, comparisons, idx, bucket.copy())
        return SearchResult(key, False, comparisons, idx, bucket.copy())

    # ---------- stats -----------------------------------------------------
    def load_factor(self) -> float:
        n = sum(len(b) for b in self.table)
        return n / self.m

    def non_empty_buckets(self) -> int:
        return sum(1 for b in self.table if b)

    def max_chain_length(self) -> int:
        return max(len(b) for b in self.table)

    def collision_count(self) -> int:
        """Number of insertions that landed on an already-occupied bucket."""
        count = 0
        for b in self.table:
            if len(b) > 1:
                count += len(b) - 1
        return count

    # ---------- display -----------------------------------------------------
    def render(self) -> str:
        lines = [f"{'Index':<6}{'Bucket contents (chain)':<40}{'Chain length'}"]
        lines.append("-" * 60)
        for i, bucket in enumerate(self.table):
            content = str(bucket) if bucket else "-- empty --"
            lines.append(f"{i:<6}{content:<40}{len(bucket)}")
        return "\n".join(lines)


def linear_search(arr: List[int], key: int) -> SearchResult:
    comparisons = 0
    for item in arr:
        comparisons += 1
        if item == key:
            return SearchResult(key, True, comparisons)
    return SearchResult(key, False, comparisons)
