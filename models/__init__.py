"""
Models Package - Library Management System

This package contains all the main model classes for the library system.
Each class represents a core entity in the system with its attributes and methods.

Classes:
    - Libro: Represents a book in the library inventory
    - Usuario: Represents a user of the library system
    - Estante: Represents a shelf with capacity constraints

Author: [Your Name]
Date: December 2025
"""

from models.libro import Libro
from models.usuario import Usuario
from models.estante import Estante

__all__ = ['Libro', 'Usuario', 'Estante']

__version__ = '1.0.0'