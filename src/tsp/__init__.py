"""Módulo de optimización combinatoria para el problema del vendedor viajero (TSP) en España."""

from .cost_model import compute_total_cost_matrix, load_tsp_data
from .ant_colony import run_ant_colony_tsp
from .genetic_tsp import run_genetic_tsp

__all__ = [
    "compute_total_cost_matrix",
    "load_tsp_data",
    "run_ant_colony_tsp",
    "run_genetic_tsp",
]
