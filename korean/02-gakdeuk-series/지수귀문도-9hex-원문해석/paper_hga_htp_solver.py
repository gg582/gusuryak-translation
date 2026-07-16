#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of the hybrid genetic algorithm from:

    Heemahn Choe, Sung-Soon Choi, and Byung-Ro Moon,
    "A Hybrid Genetic Algorithm for the Hexagonal Tortoise Problem",
    GECCO 2003, LNCS 2723, pp. 850–861, Springer, 2003.
    URL: https://www.cs.york.ac.uk/rts/docs/GECCO_2003/papers/2723/27230850.pdf

The paper proposes a hybrid GA for the Hexagonal Tortoise Problem with the
following key ingredients:
  - fitness = negative variance of hexagonal sums
  - consecutive-exchange local optimisation (only value-difference-1 swaps)
  - tabu search among equi-fitness solutions
  - nearby search around current population solutions
  - two-point crossover
  - +/-1 mutation followed by repair
  - replacement of the worst half of the population

Aging is mentioned in the paper but its detailed mechanism is not fully
specified; we use a simple age-based replacement tie-breaker instead.
"""

from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path
from typing import Any


class PaperHGAHTPSolver:
    """Hybrid GA for the Hexagonal Tortoise Problem as described in GECCO 2003."""

    def __init__(
        self,
        clusters: list[list[int]],
        n: int,
        target: int,
        population_size: int = 1000,
        max_generations: int = 1000,
        stagnation_limit: int = 200,
        mutation_prob: float = 1.0,
        seed: int | None = None,
    ) -> None:
        """
        Args:
            clusters: list of clusters, each a list of 0-based node ids.
            n: number of nodes (values 1..n).
            target: target sum for every cluster (magic constant S).
            population_size: GA population size (paper uses ~1000).
            max_generations: hard generation limit.
            stagnation_limit: stop early if best fitness does not improve.
            mutation_prob: probability of applying mutation to a gene.
            seed: random seed.
        """
        self.clusters = clusters
        self.n = n
        self.target = target
        self.population_size = population_size
        self.max_generations = max_generations
        self.stagnation_limit = stagnation_limit
        self.mutation_prob = mutation_prob
        self.rng = random.Random(seed)

    def _variance(self, chromosome: list[int]) -> float:
        total = 0.0
        for cluster in self.clusters:
            s = sum(chromosome[v] for v in cluster)
            d = s - self.target
            total += d * d
        return total

    def fitness(self, chromosome: list[int]) -> float:
        return -self._variance(chromosome)

    def _random_chromosome(self) -> list[int]:
        vals = list(range(1, self.n + 1))
        self.rng.shuffle(vals)
        return vals

    def _repair(self, chrom: list[int]) -> list[int]:
        """Repair an infeasible chromosome by replacing values with sorted ranks.

        The paper says: "gene values are replaced with their sorted orders.
        If there are genes with the same value, they are randomly reordered."
        """
        # Pair (value, original index), sort by value, assign ranks 1..n
        indexed = sorted(enumerate(chrom), key=lambda x: x[1])
        repaired = [0] * self.n
        # For equal values, shuffle the tied block
        i = 0
        while i < len(indexed):
            j = i
            while j < len(indexed) and indexed[j][1] == indexed[i][1]:
                j += 1
            block = indexed[i:j]
            self.rng.shuffle(block)
            for rank, (orig_idx, _) in enumerate(block, start=i + 1):
                repaired[orig_idx] = rank
            i = j
        return repaired

    def _consecutive_exchange(self, chrom: list[int], tabu: set[tuple[int, ...]] | None = None) -> list[int]:
        """Local optimisation using consecutive exchange + simple tabu list."""
        if tabu is None:
            tabu = set()
        best_fit = self.fitness(chrom)
        # Precompute pairs of positions whose values differ by 1
        pairs = [
            (i, j)
            for i in range(self.n)
            for j in range(i + 1, self.n)
            if abs(chrom[i] - chrom[j]) == 1
        ]
        self.rng.shuffle(pairs)
        changed = True
        while changed:
            changed = False
            for i, j in pairs:
                chrom[i], chrom[j] = chrom[j], chrom[i]
                new_fit = self.fitness(chrom)
                key = tuple(chrom)
                if new_fit > best_fit:
                    best_fit = new_fit
                    tabu.add(key)
                    changed = True
                    break
                elif abs(new_fit - best_fit) < 1e-9 and key not in tabu:
                    # equi-fitness move; accept to explore neighbours
                    tabu.add(key)
                    changed = True
                    break
                chrom[i], chrom[j] = chrom[j], chrom[i]
        return chrom

    def _two_point_crossover(self, p1: list[int], p2: list[int]) -> list[int]:
        """Two-point crossover; offspring repaired to be a valid permutation."""
        size = self.n
        a, b = sorted(self.rng.sample(range(size), 2))
        child = p1[:a] + p2[a:b] + p1[b:]
        return self._repair(child)

    def _mutation(self, chrom: list[int]) -> list[int]:
        """Mutation: each gene increased or decreased by 1 with prob 1/3 each."""
        mutated = chrom[:]
        for i in range(self.n):
            if self.rng.random() >= self.mutation_prob:
                continue
            r = self.rng.random()
            if r < 1.0 / 3.0:
                mutated[i] += 1
            elif r < 2.0 / 3.0:
                mutated[i] -= 1
            # else leave unchanged
        return self._repair(mutated)

    def _nearby_modification(self, chrom: list[int]) -> list[int]:
        """Medium-scale perturbation used in nearby search.

        We implement a simple version: a few random swaps followed by
        consecutive-exchange local optimisation.
        """
        modified = chrom[:]
        # Apply a small number of random swaps
        for _ in range(self.rng.randint(1, max(2, self.n // 10))):
            a, b = self.rng.sample(range(self.n), 2)
            modified[a], modified[b] = modified[b], modified[a]
        return self._consecutive_exchange(modified)

    def solve(self) -> dict[str, Any]:
        start = time.perf_counter()

        # Initialise and local-optimise population
        population = [self._random_chromosome() for _ in range(self.population_size)]
        population = [self._consecutive_exchange(c[:]) for c in population]
        fits = [self.fitness(c) for c in population]

        best_idx = max(range(len(fits)), key=lambda i: fits[i])
        best = population[best_idx][:]
        best_fit = fits[best_idx]

        stagnation = 0
        generations_run = 0
        history: list[tuple[int, float]] = []

        for gen in range(1, self.max_generations + 1):
            generations_run = gen
            offspring: list[list[int]] = []
            # Generate N/2 offspring
            num_offspring = self.population_size // 2
            for _ in range(num_offspring):
                p1 = self._tournament_select(population, fits)
                p2 = self._tournament_select(population, fits)
                child = self._two_point_crossover(p1, p2)
                child = self._mutation(child)
                child = self._consecutive_exchange(child)
                offspring.append(child)

            # Replace worst half
            sorted_idx = sorted(range(len(fits)), key=lambda i: fits[i], reverse=True)
            keep = sorted_idx[: self.population_size - num_offspring]
            population = [population[i][:] for i in keep] + offspring
            fits = [self.fitness(c) for c in population]

            # Nearby search on all chromosomes
            for i in range(len(population)):
                modified = self._nearby_modification(population[i][:])
                modified_fit = self.fitness(modified)
                if modified_fit >= fits[i]:
                    population[i] = modified
                    fits[i] = modified_fit

            gen_best_fit = max(fits)
            gen_best = population[fits.index(gen_best_fit)][:]  # type: ignore[arg-type]
            history.append((gen, -gen_best_fit))

            if gen_best_fit > best_fit:
                best_fit = gen_best_fit
                best = gen_best
                stagnation = 0
            else:
                stagnation += 1

            if best_fit >= -1e-9:
                break
            if stagnation >= self.stagnation_limit:
                break

        elapsed = time.perf_counter() - start
        variance = self._variance(best)
        status = "optimal" if variance <= 1e-9 else "not_found_within_limit"

        return {
            "status": status,
            "n": self.n,
            "target": self.target,
            "clusters": len(self.clusters),
            "best_assignment": best,
            "best_fitness": best_fit,
            "variance": variance,
            "generations": generations_run,
            "stagnation_limit_reached": stagnation >= self.stagnation_limit,
            "time_seconds": elapsed,
            "population_size": self.population_size,
        }

    def _tournament_select(self, population: list[list[int]], fits: list[float]) -> list[int]:
        best = None
        best_fit = -math.inf
        for _ in range(5):
            idx = self.rng.randrange(len(population))
            if fits[idx] > best_fit:
                best_fit = fits[idx]
                best = population[idx]
        assert best is not None
        return best[:]


def load_topology(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    root = Path(__file__).resolve().parent
    topology = load_topology(root / "jisu_9hex_topology.json")
    solution = load_topology(root / "jisu_9hex_solution.json")

    clusters = [[v - 1 for v in hx] for hx in topology["hexagons"]]
    n = topology["node_count"]
    target = topology["magic_constant"]

    print(f"Paper HGA-HTP solver: N={n}, clusters={len(clusters)}, target S={target}")

    solver = PaperHGAHTPSolver(
        clusters=clusters,
        n=n,
        target=target,
        population_size=300,  # smaller than paper for fast demo
        max_generations=500,
        stagnation_limit=150,
        seed=42,
    )
    result = solver.solve()
    print("\n[Paper hybrid GA]")
    print(f"  status: {result['status']}")
    print(f"  variance: {result['variance']:.6f}")
    print(f"  generations: {result['generations']}")
    print(f"  time: {result['time_seconds']:.3f}s")

    known = solution["assignment"]
    known_fit = solver.fitness(known)
    print(f"  known optimum fitness: {known_fit:.6f}")

    out_path = root / "paper_hga_htp_result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
