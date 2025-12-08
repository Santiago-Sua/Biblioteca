"""
Utilities Package - Library Management System

This package contains utility modules that provide common functionality
used across the entire application. These utilities handle cross-cutting
concerns like file operations, data validation, and helper functions.

Modules:
    - ArchivoHandler: Handles all file I/O operations including:
                     * JSON reading and writing
                     * CSV reading and parsing
                     * File existence checking
                     * Data serialization/deserialization
                     * Error handling for file operations
    
    - Validaciones: Provides validation functions for:
                   * ISBN format validation
                   * Email format validation
                   * Phone number validation
                   * Data type validation
                   * Business rule validation

Purpose:
    These utilities centralize common operations to:
    1. Reduce code duplication
    2. Ensure consistent error handling
    3. Provide reusable validation logic
    4. Simplify file operations across the system
    5. Make the codebase more maintainable

Usage:
    from utils.archivo_handler import ArchivoHandler
    from utils.validaciones import validar_isbn, validar_email
    
    handler = ArchivoHandler()
    data = handler.cargar_json("data/libros/libros.json")

Author: [Your Name]
Date: December 2025
"""

from utils.archivo_handler import ArchivoHandler
from utils.validaciones import (
    validar_isbn,
    validar_email,
    validar_telefono,
    validar_numero_positivo,
    validar_texto_no_vacio
)

__all__ = [
    'ArchivoHandler',
    'validar_isbn',
    'validar_email',
    'validar_telefono',
    'validar_numero_positivo',
    'validar_texto_no_vacio'
]

__version__ = '1.0.0'