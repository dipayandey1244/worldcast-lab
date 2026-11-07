from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class Intervention:
    """An intervention applied to one city over a time interval."""
    city: int
    start: int
    end: int
    capacity_delta: float = 0.0
    demand_multiplier: float = 1.0
    label: str = "intervention"


class TransportWorld:
    """Synthetic coupled-city transport world with known transition dynamics.

    Values are dimensionless synthetic units, not real-world measurements.
    """

    def __init__(self, cities: int = 20, seed: int = 7, coupling: float = 0.12):
        if cities < 2:
            raise ValueError("cities must be >= 2")
        self.cities = cities
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.coupling = float(coupling)
        self.population = self.rng.uniform(0.7, 1.5, cities)
        self.economy = self.rng.uniform(0.75, 1.25, cities)
        self.capacity = self.rng.uniform(0.75, 1.15, cities)
        raw = self.rng.uniform(0.0, 1.0, (cities, cities))
        np.fill_diagonal(raw, 0.0)
        self.network = raw / np.maximum(raw.sum(axis=1, keepdims=True), 1e-9)
        self.phase = self.rng.uniform(0, 2 * np.pi, cities)
        self.history: list[dict] = []

    def run(self, steps: int = 1000, interventions: list[Intervention] | None = None) -> pd.DataFrame:
        if steps < 20:
            raise ValueError("steps must be >= 20")
        interventions = interventions or []
        demand = self.population * self.economy * 100.0
        cargo = self.economy * 75.0
        for t in range(steps):
            annual = 1.0 + 0.12 * np.sin(2 * np.pi * t / 52 + self.phase)
            slow_cycle = 1.0 + 0.08 * np.sin(2 * np.pi * t / 260 + self.phase / 2)
            weather = 0.5 + 0.5 * np.sin(2 * np.pi * t / 37 + self.phase * 1.7)
            cap = self.capacity.copy()
            demand_mult = np.ones(self.cities)
            for item in interventions:
                if item.start <= t < item.end and 0 <= item.city < self.cities:
                    cap[item.city] += item.capacity_delta
                    demand_mult[item.city] *= item.demand_multiplier
            network_pressure = self.network @ (demand / np.maximum(self.capacity, 0.1))
            innovation = self.rng.normal(0, 2.2, self.cities)
            demand = (0.88 * demand + 0.12 * self.population * self.economy * 100 * annual * slow_cycle
                      + self.coupling * (network_pressure - np.mean(network_pressure)) + innovation)
            demand = np.maximum(demand * demand_mult, 1.0)
            cargo = np.maximum(0.91 * cargo + 0.09 * self.economy * 75 * slow_cycle
                               + self.rng.normal(0, 1.5, self.cities), 1.0)
            effective_capacity = np.maximum(cap * (1.0 - 0.28 * weather), 0.15)
            congestion = np.maximum(demand / (effective_capacity * 120.0) - 0.55, 0.0)
            revenue = 0.72 * demand + 0.48 * cargo - 16.0 * congestion**2
            self.economy = np.clip(self.economy + 0.0007 * (revenue / 100 - 1.0) + self.rng.normal(0, .001, self.cities), .55, 1.8)
            self.population = np.clip(self.population + 0.00015 * (demand / 100 - 1.0), .5, 2.0)
            for i in range(self.cities):
                self.history.append({
                    "time": t, "city": i, "passenger_demand": float(demand[i]),
                    "cargo_demand": float(cargo[i]), "capacity": float(cap[i]),
                    "weather_index": float(weather[i]), "congestion": float(congestion[i]),
                    "revenue": float(revenue[i]), "population_index": float(self.population[i]),
                    "economy_index": float(self.economy[i]),
                })
        return pd.DataFrame(self.history)
