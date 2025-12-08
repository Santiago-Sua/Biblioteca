"""
Recursion Package - Library Management System

This package contains recursive algorithms used to perform calculations on
book collections. Both stack recursion and tail recursion are demonstrated
as required by the project.

PROJECT REQUIREMENTS:
    1. Stack Recursion: Calculate the total value (COP) of all books by a
                       specific author using recursive function calls.
    
    2. Tail Recursion: Calculate the average weight of a collection by a
                      specific author using tail recursion with an accumulator.
                      The tail recursion logic must be demonstrated in console.

Recursion Types:
    - Stack Recursion: Traditional recursion where calculations are performed
                      during the return phase (unwinding the call stack).
                      Each recursive call waits for the next call to complete.
    
    - Tail Recursion: Optimized recursion where calculations are performed
                     before the recursive call using an accumulator. The
                     recursive call is the last operation (tail position).
                     This can be optimized by compilers to avoid stack overflow.

Technical Notes:
    While Python doesn't optimize tail recursion automatically, we implement
    it to demonstrate the concept and show how it differs from stack recursion.
    The tail recursion implementation uses an accumulator parameter to carry
    intermediate results forward.

Author: [Your Name]
Date: December 2025
"""

from recursion.recursion_pila import (
    calcular_valor_total_por_autor,
    calcular_valor_recursivo,
    demostrar_recursion_pila
)

from recursion.recursion_cola import (
    calcular_peso_promedio_por_autor,
    calcular_peso_recursivo_cola,
    demostrar_recursion_cola
)

__all__ = [
    # Stack Recursion functions
    'calcular_valor_total_por_autor',
    'calcular_valor_recursivo',
    'demostrar_recursion_pila',
    
    # Tail Recursion functions
    'calcular_peso_promedio_por_autor',
    'calcular_peso_recursivo_cola',
    'demostrar_recursion_cola'
]

__version__ = '1.0.0'