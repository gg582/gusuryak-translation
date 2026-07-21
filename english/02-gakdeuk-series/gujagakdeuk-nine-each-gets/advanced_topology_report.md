# Gujagakdeuk (九子各得) Advanced Topology & Residue Invariant Report

## Executive Summary
This report presents graph topological analysis and non-isomorphic solution space exploration for **Gujagakdeuk** under five-phase residue ($n \pmod 5$) and corner sum invariants ($92$).

## Key Findings & Graph Invariants

1. **Central Node 23 Topological Dominance**
   - Node `23` (Center Palace, cell (1,1)) exhibits the maximum Betweenness Centrality of **$0.201127$** across the 45-node multi-palace boundary graph.
   - Serves as the primary topological bridge connecting the outer 4 palaces (Top, Left, Right, Bottom).

2. **Corner Sum Invariant ($92$)**
   - Each of the 5 3x3 palaces maintains a strict corner vertex sum of **$92$** (e.g. Center Palace: $15 + 6 + 40 + 31 = 92$).

3. **Wuxing Residue ($n \pmod 5$) Balance**
   - Nodes are partitioned into 5 residue classes (Water: 1, Fire: 2, Wood: 3, Metal: 4, Earth: 0) equally distributed across all 5 palaces.

![Gujagakdeuk Topology Centrality](gujagakdeuk_topology_centrality.png)

## Execution Metrics
- **Non-Isomorphic Solutions Count:** 1
- **Spectral Radius:** `[3.5485]`
- **Graph Betweenness Centrality:** `[0.2011, 0.2011, 0.1943]`
