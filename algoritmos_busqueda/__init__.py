"""
Search Algorithms Package - Library Management System

This package contains implementations of search algorithms used throughout
the library management system. Each algorithm is optimized for specific
use cases based on data structure characteristics.

Algorithms:
    - Linear Search: Used for searching by Title or Author in the General
                    Inventory (unsorted list). This algorithm checks each
                    element sequentially until a match is found.
                    Time Complexity: O(n)
                    Use Case: Searching in unsorted data, multiple matches
    
    - Binary Search: Used for searching by ISBN in the Sorted Inventory
                    (sorted list by ISBN). This divide-and-conquer algorithm
                    is CRITICAL for the project as its result must be used
                    to verify if a returned book has pending reservations.
                    Time Complexity: O(log n)
                    Use Case: Searching in sorted data, single exact match

Project Requirement:
    Binary Search is CRITICAL - its result (position or not found) must be
    used to check if a returned book has pending reservations in the queue.
    If reservations exist, the book should be assigned to the first person
    in the waiting list according to priority (FIFO).

Author: [Your Name]
Date: December 2025
"""

from algoritmos_busqueda.busqueda_lineal import (
    busqueda_lineal,
    buscar_por_titulo,
    buscar_por_autor,
    buscar_por_atributo
)

from algoritmos_busqueda.busqueda_binaria import (
    busqueda_binaria,
    buscar_libro_por_isbn,
    verificar_y_asignar_reserva
)

__all__ = [
    # Linear Search functions
    'busqueda_lineal',
    'buscar_por_titulo',
    'buscar_por_autor',
    'buscar_por_atributo',
    
    # Binary Search functions (CRITICAL)
    'busqueda_binaria',
    'buscar_libro_por_isbn',
    'verificar_y_asignar_reserva'
]

__version__ = '1.0.0'