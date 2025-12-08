"""
Validation Utilities - Library Management System

This module provides validation functions for data validation throughout
the library system. These functions ensure data integrity and provide
consistent validation logic across all modules.

Functions:
    - validar_isbn: Validate ISBN format (ISBN-10 or ISBN-13)
    - validar_email: Validate email format
    - validar_telefono: Validate phone number format
    - validar_numero_positivo: Validate positive numeric value
    - validar_texto_no_vacio: Validate non-empty text
    - validar_rango: Validate value within range
    - validar_fecha: Validate date format
    - validar_longitud: Validate string length

Author: [Your Name]
Date: December 2025
"""

import re
from datetime import datetime


def validar_isbn(isbn):
    """
    Validate ISBN format (ISBN-10 or ISBN-13).
    
    Accepts ISBNs with or without hyphens. Validates checksum for proper ISBNs.
    
    Args:
        isbn (str): ISBN to validate
        
    Returns:
        dict: Validation result with 'valido' (bool), 'mensaje' (str), 'tipo' (str)
        
    Example:
        >>> resultado = validar_isbn("978-0-596-52068-7")
        >>> if resultado['valido']:
        ...     print("Valid ISBN-13")
    """
    if not isbn or not isinstance(isbn, str):
        return {
            'valido': False,
            'mensaje': "ISBN cannot be empty",
            'tipo': None
        }
    
    # Remove hyphens and spaces
    isbn_limpio = isbn.replace('-', '').replace(' ', '')
    
    # Check if contains only digits (and possibly X for ISBN-10)
    if not re.match(r'^[\dX]+$', isbn_limpio, re.IGNORECASE):
        return {
            'valido': False,
            'mensaje': "ISBN must contain only digits (and optionally hyphens)",
            'tipo': None
        }
    
    # Validate length
    if len(isbn_limpio) == 10:
        return _validar_isbn10(isbn_limpio)
    elif len(isbn_limpio) == 13:
        return _validar_isbn13(isbn_limpio)
    else:
        return {
            'valido': False,
            'mensaje': f"ISBN must be 10 or 13 digits (found {len(isbn_limpio)})",
            'tipo': None
        }


def _validar_isbn10(isbn):
    """
    Validate ISBN-10 format with checksum.
    
    Args:
        isbn (str): 10-character ISBN (no hyphens)
        
    Returns:
        dict: Validation result
    """
    try:
        # Calculate checksum
        suma = 0
        for i in range(9):
            suma += int(isbn[i]) * (10 - i)
        
        # Last digit can be X (representing 10)
        ultimo = isbn[9].upper()
        if ultimo == 'X':
            suma += 10
        else:
            suma += int(ultimo)
        
        # Valid if divisible by 11
        valido = (suma % 11 == 0)
        
        return {
            'valido': valido,
            'mensaje': "Valid ISBN-10" if valido else "Invalid ISBN-10 checksum",
            'tipo': 'ISBN-10'
        }
        
    except (ValueError, IndexError):
        return {
            'valido': False,
            'mensaje': "Invalid ISBN-10 format",
            'tipo': 'ISBN-10'
        }


def _validar_isbn13(isbn):
    """
    Validate ISBN-13 format with checksum.
    
    Args:
        isbn (str): 13-digit ISBN (no hyphens)
        
    Returns:
        dict: Validation result
    """
    try:
        # Calculate checksum
        suma = 0
        for i in range(12):
            multiplicador = 1 if i % 2 == 0 else 3
            suma += int(isbn[i]) * multiplicador
        
        # Check digit
        check_digit = (10 - (suma % 10)) % 10
        valido = (int(isbn[12]) == check_digit)
        
        return {
            'valido': valido,
            'mensaje': "Valid ISBN-13" if valido else "Invalid ISBN-13 checksum",
            'tipo': 'ISBN-13'
        }
        
    except (ValueError, IndexError):
        return {
            'valido': False,
            'mensaje': "Invalid ISBN-13 format",
            'tipo': 'ISBN-13'
        }


def validar_email(email):
    """
    Validate email format.
    
    Uses regex pattern to validate basic email structure.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        dict: Validation result with 'valido' (bool) and 'mensaje' (str)
        
    Example:
        >>> resultado = validar_email("user@example.com")
        >>> if resultado['valido']:
        ...     print("Valid email")
    """
    if not email or not isinstance(email, str):
        return {
            'valido': False,
            'mensaje': "Email cannot be empty"
        }
    
    # Basic email regex pattern
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(patron, email):
        return {
            'valido': True,
            'mensaje': "Valid email format"
        }
    else:
        return {
            'valido': False,
            'mensaje': "Invalid email format"
        }


def validar_telefono(telefono, pais='CO'):
    """
    Validate phone number format.
    
    Accepts various formats with optional country code and separators.
    
    Args:
        telefono (str): Phone number to validate
        pais (str, optional): Country code. Defaults to 'CO' (Colombia).
        
    Returns:
        dict: Validation result with 'valido' (bool) and 'mensaje' (str)
        
    Example:
        >>> resultado = validar_telefono("3001234567")
        >>> if resultado['valido']:
        ...     print("Valid phone")
    """
    if not telefono or not isinstance(telefono, str):
        return {
            'valido': False,
            'mensaje': "Phone number cannot be empty"
        }
    
    # Remove common separators
    telefono_limpio = re.sub(r'[\s\-\(\)\+]', '', telefono)
    
    # Check if contains only digits
    if not telefono_limpio.isdigit():
        return {
            'valido': False,
            'mensaje': "Phone number must contain only digits"
        }
    
    # Colombia: 10 digits (mobile: 3XX XXX XXXX, landline: 6XX XXX XXXX)
    if pais == 'CO':
        if len(telefono_limpio) >= 7 and len(telefono_limpio) <= 10:
            return {
                'valido': True,
                'mensaje': "Valid phone number"
            }
        else:
            return {
                'valido': False,
                'mensaje': "Colombian phone must be 7-10 digits"
            }
    
    # Generic validation: 7-15 digits
    if len(telefono_limpio) >= 7 and len(telefono_limpio) <= 15:
        return {
            'valido': True,
            'mensaje': "Valid phone number"
        }
    else:
        return {
            'valido': False,
            'mensaje': "Phone number must be 7-15 digits"
        }


def validar_numero_positivo(valor, nombre_campo="Value"):
    """
    Validate that a value is a positive number.
    
    Args:
        valor: Value to validate
        nombre_campo (str, optional): Field name for error message. Defaults to "Value".
        
    Returns:
        dict: Validation result with 'valido' (bool) and 'mensaje' (str)
        
    Example:
        >>> resultado = validar_numero_positivo(5.5, "Weight")
        >>> if resultado['valido']:
        ...     print("Valid positive number")
    """
    try:
        numero = float(valor)
        
        if numero < 0:
            return {
                'valido': False,
                'mensaje': f"{nombre_campo} cannot be negative"
            }
        
        return {
            'valido': True,
            'mensaje': f"Valid positive {nombre_campo.lower()}"
        }
        
    except (ValueError, TypeError):
        return {
            'valido': False,
            'mensaje': f"{nombre_campo} must be a number"
        }


def validar_texto_no_vacio(texto, nombre_campo="Text", min_longitud=1):
    """
    Validate that text is not empty and meets minimum length.
    
    Args:
        texto (str): Text to validate
        nombre_campo (str, optional): Field name. Defaults to "Text".
        min_longitud (int, optional): Minimum length. Defaults to 1.
        
    Returns:
        dict: Validation result with 'valido' (bool) and 'mensaje' (str)
        
    Example:
        >>> resultado = validar_texto_no_vacio("Book Title", "Title", 3)
        >>> if resultado['valido']:
        ...     print("Valid text")
    """
    if not texto or not isinstance(texto, str):
        return {
            'valido': False,
            'mensaje': f"{nombre_campo} cannot be empty"
        }
    
    texto_limpio = texto.strip()
    
    if len(texto_limpio) < min_longitud:
        return {
            'valido': False,
            'mensaje': f"{nombre_campo} must be at least {min_longitud} characters"
        }
    
    return {
        'valido': True,
        'mensaje': f"Valid {nombre_campo.lower()}"
    }


def validar_rango(valor, minimo, maximo, nombre_campo="Value"):
    """
    Validate that a value is within a specified range.
    
    Args:
        valor: Value to validate
        minimo: Minimum allowed value
        maximo: Maximum allowed value
        nombre_campo (str, optional): Field name. Defaults to "Value".
        
    Returns:
        dict: Validation result with 'valido' (bool) and 'mensaje' (str)
        
    Example:
        >>> resultado = validar_rango(25, 18, 100, "Age")
        >>> if resultado['valido']:
        ...     print("Value in range")
    """
    try:
        numero = float(valor)
        
        if numero < minimo or numero > maximo:
            return {
                'valido': False,
                'mensaje': f"{nombre_campo} must be between {minimo} and {maximo}"
            }
        
        return {
            'valido': True,
            'mensaje': f"Valid {nombre_campo.lower()} in range"
        }
        
    except (ValueError, TypeError):
        return {
            'valido': False,
            'mensaje': f"{nombre_campo} must be a number"
        }


def validar_fecha(fecha_str, formato="%Y-%m-%d"):
    """
    Validate date format.
    
    Args:
        fecha_str (str): Date string to validate
        formato (str, optional): Expected format. Defaults to "%Y-%m-%d".
        
    Returns:
        dict: Validation result with 'valido' (bool), 'mensaje' (str), 'fecha' (datetime)
        
    Example:
        >>> resultado = validar_fecha("2025-12-07")
        >>> if resultado['valido']:
        ...     print(f"Valid date: {resultado['fecha']}")
    """
    if not fecha_str or not isinstance(fecha_str, str):
        return {
            'valido': False,
            'mensaje': "Date cannot be empty",
            'fecha': None
        }
    
    try:
        fecha = datetime.strptime(fecha_str, formato)
        
        return {
            'valido': True,
            'mensaje': "Valid date format",
            'fecha': fecha
        }
        
    except ValueError:
        return {
            'valido': False,
            'mensaje': f"Invalid date format. Expected: {formato}",
            'fecha': None
        }


def validar_longitud(texto, min_longitud=None, max_longitud=None, nombre_campo="Text"):
    """
    Validate string length within specified bounds.
    
    Args:
        texto (str): Text to validate
        min_longitud (int, optional): Minimum length. Defaults to None.
        max_longitud (int, optional): Maximum length. Defaults to None.
        nombre_campo (str, optional): Field name. Defaults to "Text".
        
    Returns:
        dict: Validation result with 'valido' (bool) and 'mensaje' (str)
        
    Example:
        >>> resultado = validar_longitud("Title", min_longitud=3, max_longitud=100)
        >>> if resultado['valido']:
        ...     print("Valid length")
    """
    if not isinstance(texto, str):
        return {
            'valido': False,
            'mensaje': f"{nombre_campo} must be text"
        }
    
    longitud = len(texto)
    
    if min_longitud is not None and longitud < min_longitud:
        return {
            'valido': False,
            'mensaje': f"{nombre_campo} must be at least {min_longitud} characters"
        }
    
    if max_longitud is not None and longitud > max_longitud:
        return {
            'valido': False,
            'mensaje': f"{nombre_campo} cannot exceed {max_longitud} characters"
        }
    
    return {
        'valido': True,
        'mensaje': f"Valid {nombre_campo.lower()} length"
    }


def validar_entero_positivo(valor, nombre_campo="Value"):
    """
    Validate that a value is a positive integer.
    
    Args:
        valor: Value to validate
        nombre_campo (str, optional): Field name. Defaults to "Value".
        
    Returns:
        dict: Validation result with 'valido' (bool) and 'mensaje' (str)
        
    Example:
        >>> resultado = validar_entero_positivo(5, "Stock")
        >>> if resultado['valido']:
        ...     print("Valid positive integer")
    """
    try:
        numero = int(valor)
        
        if numero < 0:
            return {
                'valido': False,
                'mensaje': f"{nombre_campo} cannot be negative"
            }
        
        return {
            'valido': True,
            'mensaje': f"Valid positive integer {nombre_campo.lower()}"
        }
        
    except (ValueError, TypeError):
        return {
            'valido': False,
            'mensaje': f"{nombre_campo} must be an integer"
        }


def validar_multiples_campos(validaciones):
    """
    Validate multiple fields at once.
    
    Args:
        validaciones (dict): Dictionary with field names as keys and validation results as values
        
    Returns:
        dict: Combined validation result with all errors
        
    Example:
        >>> validaciones = {
        ...     'isbn': validar_isbn("123"),
        ...     'email': validar_email("invalid"),
        ...     'stock': validar_entero_positivo(-1)
        ... }
        >>> resultado = validar_multiples_campos(validaciones)
        >>> if not resultado['valido']:
        ...     for error in resultado['errores']:
        ...         print(error)
    """
    errores = []
    todos_validos = True
    
    for campo, resultado in validaciones.items():
        if not resultado['valido']:
            todos_validos = False
            errores.append(f"{campo}: {resultado['mensaje']}")
    
    return {
        'valido': todos_validos,
        'errores': errores,
        'mensaje': "All validations passed" if todos_validos else f"{len(errores)} validation error(s)"
    }