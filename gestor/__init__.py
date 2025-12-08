"""
Gestor (Manager) Package - Library Management System

This package contains all the manager classes that coordinate the business
logic of the library system. Each manager handles a specific domain and
integrates the models, data structures, and algorithms.

Managers:
    - GestorInventario: Manages book inventory including:
                       * General Inventory (unsorted, maintains load order)
                       * Sorted Inventory (sorted by ISBN for binary search)
                       * Book CRUD operations
                       * Search algorithms integration
                       * Sorting algorithms integration
    
    - GestorUsuarios: Manages library users including:
                     * User registration and authentication
                     * User CRUD operations
                     * User status management (active/inactive)
                     * Loan capacity tracking
    
    - GestorPrestamos: Manages book loans including:
                      * Loan creation and validation
                      * Return processing
                      * Loan history (using Pila/Stack per user)
                      * Integration with reservation queue
                      * CRITICAL: Uses binary search to check reservations on return
    
    - GestorReservas: Manages book reservations including:
                     * Reservation queue (using Cola/Queue)
                     * FIFO priority processing
                     * Reservation cancellation
                     * Integration with loan processing

Architecture:
    Each manager acts as a facade that:
    1. Coordinates between models and data structures
    2. Implements business rules and validations
    3. Integrates algorithms at appropriate points
    4. Provides a clean API for the UI layer
    5. Handles data persistence through utils.archivo_handler

Data Flow:
    UI Layer → Gestor Layer → (Models + Algorithms + Structures) → Data Layer

Author: [Your Name]
Date: December 2025
"""

from gestor.gestor_inventario import GestorInventario
from gestor.gestor_usuarios import GestorUsuarios
from gestor.gestor_prestamos import GestorPrestamos
from gestor.gestor_reservas import GestorReservas

__all__ = [
    'GestorInventario',
    'GestorUsuarios',
    'GestorPrestamos',
    'GestorReservas'
]

__version__ = '1.0.0'