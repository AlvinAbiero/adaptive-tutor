import sys

from memory_index import MemoryIndex
from tutor_memory_data import MEMORIES, QUERIES

K = 3
TOKENS_PER_MEMORY = 19   # rough figure measured on Day 41

CONFIGS = {
    "similarity only": dict(w_sim=1.0, w_rec=0.0, w_imp=0.0),
    "+ recency": dict(w_sim=1.0, w_rec=0.2, w_imp=0.0),
    "+ recency + importance": dict(w_sim=1.0, w_rec=0.2, w_imp=0.1),
}


def evaluate(index, cfg, detail):
    hits, recalls, stale_ok = 0, [], None
    for q in QUERIES:
        top = index.search(q["text"], k=K, **cfg)
        ids = [m["id"] for _, _, m in top]
        got = [r for r in q["relevant"] if r in ids]
        hits += bool(got)
        recalls.append(len(got) / len(q["relevant"]))
        if q.get("stale"):
            order = [m["id"] for _, _, m in index.search(q["text"], k=len(MEMORIES), **cfg)]
            stale_ok = order.index(q["relevant"][0]) < order.index(q["stale"][0])
        if detail:
            mark = "ok " if len(got) == len(q["relevant"]) else "miss"
            print(f"   {q['id']} {mark} expected {q['relevant']} got {ids}")
    return hits / len(QUERIES), sum(recalls) / len(recalls), stale_ok


def main():
    detail = "--detail" in sys.argv
    index = MemoryIndex(MEMORIES)
    print(f"{len(MEMORIES)} memories, {len(QUERIES)} queries, top-{K}\n")
    print(f"{'config':<26} {'hit@3':>6} {'recall@3':>9}  new beats stale")
    print("-" * 62)
    for name, cfg in CONFIGS.items():
        if detail:
            print(f"\n{name}")
        hit, recall, stale = evaluate(index, cfg, detail)
        print(f"{name:<26} {hit:>6.2f} {recall:>9.2f}  {'yes' if stale else 'NO'}")
    print(f"\nprompt cost: top-{K} is about {K * TOKENS_PER_MEMORY} tokens per call, "
          f"all {len(MEMORIES)} memories would be about {len(MEMORIES) * TOKENS_PER_MEMORY}")


if __name__ == "__main__":
    main()