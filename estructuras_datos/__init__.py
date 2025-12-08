"""
Data Structures Package - Library Management System

This package contains custom implementations of fundamental data structures
used throughout the library management system. All structures are implemented
using Object-Oriented Programming principles.

Classes:
    - Pila: Stack (LIFO) implementation for loan history management
    - Cola: Queue (FIFO) implementation for reservation waiting list

The Pila (Stack) is used to manage the loan history per user, where the most
recent loan is at the top and can be accessed first (LIFO - Last In, First Out).

The Cola (Queue) is used to manage the waiting list for books that are out of
stock. Users are enqueued in order and dequeued following FIFO (First In, First Out)
when a book becomes available.

Author: [Your Name]
Date: December 2025
"""

from estructuras_datos.pila import Pila
from estructuras_datos.cola import Cola

__all__ = ['Pila', 'Cola']

__version__ = '1.0.0'