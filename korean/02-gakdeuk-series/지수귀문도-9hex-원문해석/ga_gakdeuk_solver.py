#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A generic genetic-algorithm solver for "each-gets" (gakdeuk / 各得) puzzles.

Given N nodes, clusters (each of which must sum to the same magic constant S),
and the numbers 1..N, this solver evolves permutations to minimise the
variance of cluster sums.  If a perfect solution exists, the variance becomes
zero and the algorithm reports it.  If no improvement is seen for a long time,
it reports that no solution was found within the budget.

The design is intentionally general so it can be applied to any gakdeuk-style
puzzle: Hexagonal Tortoise, Nakseo Sagudo, Ojagakdeuk, etc.
"""

from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path
from typing import Any


class GAGakdeukSolver:
    """Permutation-based GA for equal-cluster-sum problems."""

    def __init__(
        self,
        clusters: list[list[int]],
        n: int,
        target: int,
        population_size: int = 200,
        max_generations: int = 2000,
        crossover_rate: float = 0.9,
        mutation_rate: float = 0.2,
        tournament_size: int = 5,
        elitism_count: int = 2,
        local_search: bool = True,
        consecutive_only: bool = False,
        stagnation_limit: int = 300,
        seed: int | None = None,
    ) -> None:
        """
        Args:
            clusters: list of clusters, each cluster is a list of 0-based node ids.
            n: number of nodes (values are 1..n).
            target: target sum for every cluster (magic constant S).
            population_size: GA population size.
            max_generations: hard generation limit.
            crossover_rate: probability of applying PMX crossover.
            mutation_rate: probability of applying swap mutation.
            tournament_size: tournament selection size.
            elitism_count: number of best individuals copied to next generation.
            local_search: whether to apply hill-climbing swap after each operator.
            consecutive_only: if True, local search only swaps values differing by 1.
            stagnation_limit: stop early if best fitness does not improve for this
                many generations.
            seed: random seed for reproducibility.
        """
        self.clusters = clusters
        self.n = n
        self.target = target
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism_count = elitism_count
        self.local_search = local_search
        self.consecutive_only = consecutive_only
        self.stagnation_limit = stagnation_limit
        self.rng = random.Random(seed)

    def _variance(self, chromosome: list[int]) -> float:
        """Sum of squared deviations of cluster sums from the target."""
        total = 0.0
        for cluster in self.clusters:
            s = sum(chromosome[v] for v in cluster)
            d = s - self.target
            total += d * d
        return total

    def fitness(self, chromosome: list[int]) -> float:
        """Higher is better.  Zero variance -> fitness 0 (optimal)."""
        return -self._variance(chromosome)

    def _random_chromosome(self) -> list[int]:
        vals = list(range(1, self.n + 1))
        self.rng.shuffle(vals)
        return vals

    def _initial_population(self) -> list[list[int]]:
        return [self._random_chromosome() for _ in range(self.population_size)]

    def _tournament_select(self, population: list[list[int]], fits: list[float]) -> list[int]:
        best = None
        best_fit = -math.inf
        for _ in range(self.tournament_size):
            idx = self.rng.randrange(len(population))
            if fits[idx] > best_fit:
                best_fit = fits[idx]
                best = population[idx]
        assert best is not None
        return best[:]

    def _pmx_crossover(self, p1: list[int], p2: list[int]) -> list[int]:
        """Partially mapped crossover, preserving permutation validity."""
        size = len(p1)
        a, b = sorted(self.rng.sample(range(size), 2))
        child = [0] * size
        # copy segment from p1
        child[a:b] = p1[a:b]
        # mapping from p1 segment values to p2 segment values
        mapping: dict[int, int] = {}
        for i in range(a, b):
            mapping[p1[i]] = p2[i]
        # fill remaining positions from p2
        for i in list(range(a)) + list(range(b, size)):
            val = p2[i]
            while val in mapping:
                val = mapping[val]
            child[i] = val
        return child

    def _swap_mutation(self, chrom: list[int]) -> list[int]:
        if self.rng.random() >= self.mutation_rate:
            return chrom
        a, b = self.rng.sample(range(len(chrom)), 2)
        chrom[a], chrom[b] = chrom[b], chrom[a]
        return chrom

    def _local_search_swap(self, chrom: list[int]) -> list[int]:
        """Greedy first-improvement swap local search."""
        improved = True
        best_fit = self.fitness(chrom)
        # candidate pairs
        if self.consecutive_only:
            # only pairs whose values differ by 1
            pairs = []
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    if abs(chrom[i] - chrom[j]) == 1:
                        pairs.append((i, j))
            # fallback if no consecutive pair exists (should not happen for n>1)
            if not pairs:
                pairs = [(i, j) for i in range(self.n) for j in range(i + 1, self.n)]
        else:
            pairs = [(i, j) for i in range(self.n) for j in range(i + 1, self.n)]

        # shuffle to avoid bias
        self.rng.shuffle(pairs)
        while improved:
            improved = False
            for i, j in pairs:
                chrom[i], chrom[j] = chrom[j], chrom[i]
                new_fit = self.fitness(chrom)
                if new_fit > best_fit:
                    best_fit = new_fit
                    improved = True
                    break
                # revert
                chrom[i], chrom[j] = chrom[j], chrom[i]
        return chrom

    def solve(self) -> dict[str, Any]:
        """Run the GA and return the result dictionary."""
        start = time.perf_counter()
        population = self._initial_population()
        fits = [self.fitness(c) for c in population]

        best_idx = max(range(len(fits)), key=lambda i: fits[i])
        best = population[best_idx][:]
        best_fit = fits[best_idx]

        generations_run = 0
        stagnation = 0
        history: list[tuple[int, float]] = []

        for gen in range(1, self.max_generations + 1):
            generations_run = gen
            new_population: list[list[int]] = []
            # elitism
            sorted_idx = sorted(range(len(fits)), key=lambda i: fits[i], reverse=True)
            new_population.extend(population[i][:] for i in sorted_idx[: self.elitism_count])

            while len(new_population) < self.population_size:
                p1 = self._tournament_select(population, fits)
                p2 = self._tournament_select(population, fits)
                if self.rng.random() < self.crossover_rate:
                    child = self._pmx_crossover(p1, p2)
                else:
                    child = p1[:]
                child = self._swap_mutation(child)
                if self.local_search:
                    child = self._local_search_swap(child)
                new_population.append(child)

            population = new_population
            fits = [self.fitness(c) for c in population]

            gen_best_fit = max(fits)
            gen_best = population[fits.index(gen_best_fit)][:]  # type: ignore[arg-type]
            history.append((gen, -gen_best_fit))

            if gen_best_fit > best_fit:
                best_fit = gen_best_fit
                best = gen_best
                stagnation = 0
            else:
                stagnation += 1

            if best_fit >= -1e-9:  # perfect solution
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
            "local_search": self.local_search,
            "consecutive_only": self.consecutive_only,
        }


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

    print(f"GA gakdeuk solver: N={n}, clusters={len(clusters)}, target S={target}")

    # Run with normal 2-opt style local search
    solver = GAGakdeukSolver(
        clusters=clusters,
        n=n,
        target=target,
        population_size=200,
        max_generations=2000,
        local_search=True,
        consecutive_only=False,
        stagnation_limit=300,
        seed=42,
    )
    result = solver.solve()
    print("\n[GA with full swap local search]")
    print(f"  status: {result['status']}")
    print(f"  variance: {result['variance']:.6f}")
    print(f"  generations: {result['generations']}")
    print(f"  time: {result['time_seconds']:.3f}s")

    # Verify against known optimum if available
    known = solution["assignment"]
    known_fit = solver.fitness(known)
    print(f"  known optimum fitness: {known_fit:.6f}")

    out_path = root / "ga_gakdeuk_result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
