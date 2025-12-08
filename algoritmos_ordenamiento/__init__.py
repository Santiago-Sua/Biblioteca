"""
Sorting Algorithms Package - Library Management System

This package contains implementations of sorting algorithms used throughout
the library management system. All algorithms are implemented following
best practices and are fully documented.

Algorithms:
    - Insertion Sort: Used to maintain the Sorted Inventory (by ISBN) whenever
                     a new book is added to the system. This ensures the list
                     is always ready for Binary Search operations.
                     Time Complexity: O(n²) worst case, O(n) best case
    
    - Merge Sort: Used to generate global inventory reports sorted by value (COP).
                 This recursive divide-and-conquer algorithm provides consistent
                 O(n log n) performance regardless of input order.
                 Time Complexity: O(n log n) in all cases

Usage:
    The Insertion Sort is called incrementally as books are added to maintain
    order, while Merge Sort is used for one-time report generation where the
    entire inventory needs to be sorted by a different criteria.

Author: [Your Name]
Date: December 2025
"""

from algoritmos_ordenamiento.insercion import ordenamiento_insercion, insertar_ordenado
from algoritmos_ordenamiento.merge_sort import ordenamiento_mezcla, merge_sort_por_atributo

__all__ = [
    'ordenamiento_insercion',
    'insertar_ordenado',
    'ordenamiento_mezcla',
    'merge_sort_por_atributo'
]

__version__ = '1.0.0'