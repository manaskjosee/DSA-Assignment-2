"""
main.py
-------
Runs the full Song-ID hashing experiment:
  a) builds the hash table (Division Method), showing the table after
     EVERY insertion and flagging collisions
  b) searches for a set of IDs using (1) hashing and (2) plain linear
     search over the original array, counting comparisons for both
  c) prints load factor / collision statistics for the analysis section

Run with:  python3 main.py
"""

from hash_table import DivisionHashTable, linear_search

SONG_IDS = [105, 210, 315, 420, 525, 630, 735, 840]
TABLE_SIZE = 10          # m = 10  (chosen so the assignment's "identify
                          #          collisions" requirement is satisfiable
                          #          and to expose an important design lesson
                          #          -- see README Part (c))

SEARCH_IDS = [630, 735, 105, 999, 615]   # mix of present / absent / best / worst case


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    # ---------------- Part (a): build + show table after each insertion ----
    section("PART (a): BUILDING THE HASH TABLE  (Division Method, m=10)")
    ht = DivisionHashTable(TABLE_SIZE)
    for song_id in SONG_IDS:
        idx = ht.insert(song_id)
        print("\n" + ht.insert_log[-1])
        print(ht.render())

    section("Collision summary after all insertions")
    print(f"Total insertions            : {len(SONG_IDS)}")
    print(f"Table size (m)              : {TABLE_SIZE}")
    print(f"Non-empty buckets           : {ht.non_empty_buckets()}")
    print(f"Total collisions            : {ht.collision_count()}")
    print(f"Longest chain (max probes)  : {ht.max_chain_length()}")
    print(f"Load factor (n/m)           : {ht.load_factor():.2f}")

    # ---------------- Part (b): search comparisons ---------------------------
    section("PART (b): SEARCH COMPARISON -- Hashing vs Linear Search")
    header = f"{'Key':<8}{'Hash: found':<14}{'Hash comparisons':<20}{'Linear: found':<16}{'Linear comparisons'}"
    print(header)
    print("-" * len(header))
    rows = []
    for key in SEARCH_IDS:
        hres = ht.search(key)
        lres = linear_search(SONG_IDS, key)
        rows.append((key, hres, lres))
        print(f"{key:<8}{str(hres.found):<14}{hres.comparisons:<20}{str(lres.found):<16}{lres.comparisons}")

    # ---------------- Part (c): quick derived stats -----------------------------
    section("PART (c): DERIVED PERFORMANCE STATS")
    n = len(SONG_IDS)
    alpha = n / TABLE_SIZE
    avg_hash_comp = sum(r[1].comparisons for r in rows) / len(rows)
    avg_lin_comp = sum(r[2].comparisons for r in rows) / len(rows)
    print(f"n (keys)                          : {n}")
    print(f"m (table size)                    : {TABLE_SIZE}")
    print(f"Load factor alpha = n/m           : {alpha:.2f}")
    print(f"Theoretical avg comparisons (chaining, unsuccessful) ~ 1 + alpha : {1+alpha:.2f}")
    print(f"Observed avg comparisons (hashing, this search set)  : {avg_hash_comp:.2f}")
    print(f"Observed avg comparisons (linear search, this search set) : {avg_lin_comp:.2f}")

    # ---------------- Bonus: what a better table size (prime m) would do -----
    section("BONUS: Same keys with a PRIME table size (m=11) -- design fix")
    ht2 = DivisionHashTable(11)
    ht2.build(SONG_IDS)
    print(ht2.render())
    print(f"\nCollisions with m=11 : {ht2.collision_count()}")
    print(f"Load factor with m=11 : {ht2.load_factor():.2f}")


if __name__ == "__main__":
    main()
