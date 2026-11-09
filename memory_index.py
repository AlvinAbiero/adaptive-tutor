import math

from embed import embed


def _unit(v):
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


class MemoryIndex:
    """A minimal vector store: vectors + metadata + exact nearest-neighbour search."""

    def __init__(self, memories):
        self.memories = memories
        # nomic-embed-text is trained with task prefixes; leaving them off quietly lowers quality
        vectors = embed(["search_document: " + m["text"] for m in memories])
        self.vectors = [_unit(v) for v in vectors]
        self._qcache = {}

    def _query_vector(self, query):
        if query not in self._qcache:
            self._qcache[query] = _unit(embed(["search_query: " + query])[0])
        return self._qcache[query]

    def search(self, query, k=3, w_sim=1.0, w_rec=0.0, w_imp=0.0, half_life=30.0):
        q = self._query_vector(query)
        scored = []
        for m, v in zip(self.memories, self.vectors):
            sim = sum(a * b for a, b in zip(q, v))
            recency = 0.5 ** (m["age_days"] / half_life)
            importance = m["importance"] / 5
            score = w_sim * sim + w_rec * recency + w_imp * importance
            scored.append((score, sim, m))
        scored.sort(key=lambda s: -s[0])
        return scored[:k]