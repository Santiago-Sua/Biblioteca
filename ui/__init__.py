"""
User Interface Package - Library Management System

This package contains all the graphical user interface components for the
library management system. Each module represents a window or view that
provides specific functionality to the user.

Windows/Views:
    - VentanaPrincipal: Main application window (handled by main.py)
    
    - LibrosWindow: Books management interface
                   * View all books (General and Sorted inventories)
                   * Create new books
                   * Update book information
                   * Delete books
                   * Search by title, author, or ISBN
                   * Generate reports by value
    
    - UsuariosWindow: Users management interface
                     * View all users
                     * Register new users
                     * Update user information
                     * Activate/deactivate users
                     * Delete users
                     * View user statistics
    
    - PrestamosWindow: Loans management interface
                      * Create new loans
                      * Process book returns
                      * View loan history per user
                      * View active loans
                      * Loan statistics
    
    - ReservasWindow: Reservations management interface
                     * Create reservations (only for out-of-stock books)
                     * Cancel reservations
                     * View reservation queue
                     * View user's reservations
                     * Reservation statistics
    
    - EstanteriaWindow: Shelf optimization interface
                       * Brute force analysis (risky combinations)
                       * Backtracking optimization (maximize value)
                       * View shelf configurations
                       * Safety reports
    
    - ReportesWindow: Reports and analytics interface
                     * Inventory reports (sorted by value)
                     * Loan statistics
                     * Reservation statistics
                     * Recursive calculations (value by author, avg weight)
                     * Export reports to CSV/JSON

Design Pattern:
    Each window class follows a consistent pattern:
    1. Receives parent container and archivo_handler
    2. Creates its own frame inside the parent
    3. Organizes UI with sub-frames (forms, tables, buttons)
    4. Connects to appropriate gestor (manager) classes
    5. Provides feedback to user (success/error messages)

Technology Stack:
    - tkinter: Base GUI framework
    - ttk/ttkbootstrap: Modern themed widgets
    - messagebox: User notifications
    - Treeview: Tables for displaying data

Author: [Your Name]
Date: December 2025
"""

from ui.ventana_libros import LibrosWindow
from ui.ventana_usuarios import UsuariosWindow
from ui.ventana_prestamos import PrestamosWindow
from ui.ventana_reservas import ReservasWindow
from ui.ventana_estanteria import EstanteriaWindow
from ui.ventana_reportes import ReportesWindow

__all__ = [
    'LibrosWindow',
    'UsuariosWindow',
    'PrestamosWindow',
    'ReservasWindow',
    'EstanteriaWindow',
    'ReportesWindow'
]

__version__ = '1.0.0'