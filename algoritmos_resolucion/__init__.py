"""
Problem Resolution Algorithms Package - Library Management System

This package contains algorithms for solving optimization and constraint
problems related to shelf management in the library. These algorithms are
part of the Shelf Module (Módulo de Estantería) of the project.

PROJECT CONTEXT:
    The library has physical shelves with a maximum weight capacity of 8 kg.
    These algorithms help optimize book placement and identify potential risks.

Algorithms:
    - Brute Force (Deficient Shelf): Exhaustively finds ALL combinations of
                                     4 books that exceed the 8 kg risk threshold.
                                     This identifies potentially dangerous shelf
                                     configurations that should be avoided.
                                     Time Complexity: O(n^4) - explores all combinations
    
    - Backtracking (Optimal Shelf): Finds the combination of books that maximizes
                                   total value (COP) while respecting the 8 kg
                                   weight constraint. Uses pruning to eliminate
                                   invalid branches early.
                                   Time Complexity: O(2^n) worst case, but pruning
                                   significantly reduces actual search space

Use Cases:
    - Brute Force: Safety inspection to identify risky shelf configurations
    - Backtracking: Optimize shelf value while maintaining safety constraints

Author: [Your Name]
Date: December 2025
"""

from algoritmos_resolucion.fuerza_bruta import (
    encontrar_combinaciones_riesgosas,
    generar_combinaciones_cuatro_libros,
    analizar_seguridad_estantes
)

from algoritmos_resolucion.backtracking import (
    optimizar_estante,
    encontrar_mejor_combinacion,
    backtracking_con_demostracion
)

__all__ = [
    # Brute Force functions
    'encontrar_combinaciones_riesgosas',
    'generar_combinaciones_cuatro_libros',
    'analizar_seguridad_estantes',
    
    # Backtracking functions
    'optimizar_estante',
    'encontrar_mejor_combinacion',
    'backtracking_con_demostracion'
]

# Project constants
CAPACIDAD_MAXIMA_ESTANTE = 8.0  # Maximum weight capacity in kilograms
UMBRAL_RIESGO = 8.0  # Risk threshold for brute force analysis

__version__ = '1.0.0'