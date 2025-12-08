"""
Insertion Sort Algorithm - Library Management System

This module implements the Insertion Sort algorithm used to maintain the
Sorted Inventory list. Every time a new book is added to the system, this
algorithm ensures the list remains sorted by ISBN in ascending order.

The Insertion Sort is ideal for this use case because:
1. It's efficient for small additions to an already sorted list
2. It has O(n) best-case performance when the list is nearly sorted
3. It's simple and maintains stability

Algorithm Explanation:
    The algorithm works by building the sorted list one element at a time.
    For each new element, it finds the correct position in the already sorted
    portion and inserts it there, shifting other elements as needed.

Time Complexity:
    - Best Case: O(n) - when list is already sorted
    - Average Case: O(n²)
    - Worst Case: O(n²) - when list is reverse sorted

Space Complexity: O(1) - sorts in place

Author: [Your Name]
Date: December 2025
"""


def ordenamiento_insercion(lista_libros, clave='isbn', reverso=False):
    """
    Sort a list of books using Insertion Sort algorithm.
    
    This function sorts a list of book objects (or dictionaries) based on
    a specified attribute key. The sort is performed in-place, modifying
    the original list.
    
    Args:
        lista_libros (list): List of book objects or dictionaries to sort
        clave (str, optional): Attribute/key to sort by. Defaults to 'isbn'.
        reverso (bool, optional): If True, sort in descending order. Defaults to False.
        
    Returns:
        list: The same list, now sorted (modified in-place)
        
    Example:
        >>> libros = [libro1, libro2, libro3]
        >>> ordenamiento_insercion(libros, clave='isbn')
        >>> # Now libros is sorted by ISBN in ascending order
    """
    n = len(lista_libros)
    
    # Iterate through the list starting from the second element
    for i in range(1, n):
        # Store the current element to be inserted
        elemento_actual = lista_libros[i]
        
        # Get the value of the key to compare
        if isinstance(elemento_actual, dict):
            valor_actual = elemento_actual.get(clave, "")
        else:
            valor_actual = getattr(elemento_actual, clave, "")
        
        # Find the correct position for the current element
        j = i - 1
        
        # Shift elements to the right until we find the correct position
        while j >= 0:
            # Get the value to compare from the element at position j
            if isinstance(lista_libros[j], dict):
                valor_comparacion = lista_libros[j].get(clave, "")
            else:
                valor_comparacion = getattr(lista_libros[j], clave, "")
            
            # Determine if we need to continue shifting
            if reverso:
                # For descending order
                if valor_comparacion < valor_actual:
                    break
            else:
                # For ascending order
                if valor_comparacion <= valor_actual:
                    break
            
            # Shift element to the right
            lista_libros[j + 1] = lista_libros[j]
            j -= 1
        
        # Insert the current element in its correct position
        lista_libros[j + 1] = elemento_actual
    
    return lista_libros


def insertar_ordenado(lista_ordenada, nuevo_libro, clave='isbn'):
    """
    Insert a new book into an already sorted list maintaining order.
    
    This function is optimized for inserting a single element into an
    already sorted list. It finds the correct position and inserts the
    book there, which is more efficient than re-sorting the entire list.
    
    This is the CRITICAL function for the project requirement: maintaining
    the Sorted Inventory whenever a new book is added.
    
    Args:
        lista_ordenada (list): Already sorted list of books
        nuevo_libro: Book object or dictionary to insert
        clave (str, optional): Attribute/key to maintain sort by. Defaults to 'isbn'.
        
    Returns:
        list: The list with the new book inserted in the correct position
        
    Example:
        >>> inventario_ordenado = [libro1, libro2, libro4]
        >>> insertar_ordenado(inventario_ordenado, libro3, clave='isbn')
        >>> # Now inventario_ordenado has libro3 in the correct position
        
    Time Complexity: O(n) - needs to find position and potentially shift elements
    """
    # Get the value to insert
    if isinstance(nuevo_libro, dict):
        valor_nuevo = nuevo_libro.get(clave, "")
    else:
        valor_nuevo = getattr(nuevo_libro, clave, "")
    
    # Find the correct position to insert
    posicion = 0
    for i, libro in enumerate(lista_ordenada):
        # Get the value to compare
        if isinstance(libro, dict):
            valor_actual = libro.get(clave, "")
        else:
            valor_actual = getattr(libro, clave, "")
        
        # If current value is greater, we found the position
        if valor_actual > valor_nuevo:
            posicion = i
            break
        posicion = i + 1
    
    # Insert the new book at the found position
    lista_ordenada.insert(posicion, nuevo_libro)
    
    return lista_ordenada


def verificar_ordenamiento(lista_libros, clave='isbn'):
    """
    Verify if a list of books is correctly sorted.
    
    This utility function checks if the list is sorted in ascending order
    by the specified key. Useful for testing and validation.
    
    Args:
        lista_libros (list): List of books to verify
        clave (str, optional): Attribute/key to check. Defaults to 'isbn'.
        
    Returns:
        bool: True if list is sorted, False otherwise
        
    Example:
        >>> if verificar_ordenamiento(inventario_ordenado):
        ...     print("Inventory is correctly sorted")
    """
    if len(lista_libros) <= 1:
        return True
    
    for i in range(len(lista_libros) - 1):
        # Get values to compare
        if isinstance(lista_libros[i], dict):
            valor_actual = lista_libros[i].get(clave, "")
            valor_siguiente = lista_libros[i + 1].get(clave, "")
        else:
            valor_actual = getattr(lista_libros[i], clave, "")
            valor_siguiente = getattr(lista_libros[i + 1], clave, "")
        
        # Check if order is correct
        if valor_actual > valor_siguiente:
            return False
    
    return True


def obtener_posicion_insercion(lista_ordenada, valor, clave='isbn'):
    """
    Find the position where a value should be inserted in a sorted list.
    
    This helper function returns the index where a new element with the
    given value should be inserted to maintain sorted order.
    
    Args:
        lista_ordenada (list): Sorted list of books
        valor: Value to find position for
        clave (str, optional): Attribute/key being sorted by. Defaults to 'isbn'.
        
    Returns:
        int: Index position where the element should be inserted
        
    Example:
        >>> pos = obtener_posicion_insercion(inventario, "978-0-123456-78-9")
        >>> print(f"New book should be inserted at position {pos}")
    """
    for i, libro in enumerate(lista_ordenada):
        if isinstance(libro, dict):
            valor_actual = libro.get(clave, "")
        else:
            valor_actual = getattr(libro, clave, "")
        
        if valor_actual > valor:
            return i
    
    return len(lista_ordenada)


# Demonstration function for educational purposes
def demostrar_insercion(lista_libros, clave='isbn'):
    """
    Demonstrate the Insertion Sort algorithm step by step.
    
    This function prints each step of the sorting process for educational
    purposes, showing how elements are inserted one by one.
    
    Args:
        lista_libros (list): List of books to sort
        clave (str, optional): Attribute to sort by. Defaults to 'isbn'.
        
    Note:
        This function prints to console and is intended for demonstration only.
    """
    print("=== Insertion Sort Demonstration ===")
    print(f"Sorting by: {clave}")
    print(f"Initial list size: {len(lista_libros)}")
    print()
    
    n = len(lista_libros)
    
    for i in range(1, n):
        elemento_actual = lista_libros[i]
        
        if isinstance(elemento_actual, dict):
            valor_actual = elemento_actual.get(clave, "")
        else:
            valor_actual = getattr(elemento_actual, clave, "")
        
        print(f"Step {i}: Inserting element with {clave} = {valor_actual}")
        
        j = i - 1
        movimientos = 0
        
        while j >= 0:
            if isinstance(lista_libros[j], dict):
                valor_comparacion = lista_libros[j].get(clave, "")
            else:
                valor_comparacion = getattr(lista_libros[j], clave, "")
            
            if valor_comparacion <= valor_actual:
                break
            
            lista_libros[j + 1] = lista_libros[j]
            movimientos += 1
            j -= 1
        
        lista_libros[j + 1] = elemento_actual
        print(f"  -> Moved {movimientos} elements, inserted at position {j + 1}")
        print()
    
    print("=== Sorting Complete ===")
    return lista_libros