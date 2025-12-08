"""
Binary Search Algorithm - Library Management System

This module implements the Binary Search algorithm used to search for books
by ISBN in the Sorted Inventory (list sorted by ISBN in ascending order).
This is a CRITICAL component of the project.

CRITICAL PROJECT REQUIREMENT:
    The result of binary search (position or not found) MUST be used to verify
    if a returned book has pending reservations in the queue. If reservations
    exist, the book must be assigned to the first person in the waiting list
    according to FIFO priority.

The Binary Search is appropriate for this use case because:
1. The Sorted Inventory is maintained in ascending order by ISBN
2. It provides O(log n) performance - much faster than linear search
3. ISBN is unique and provides exact match requirements
4. The result position can be used for additional operations

Algorithm Explanation:
    The algorithm works by repeatedly dividing the search interval in half.
    It compares the target value with the middle element. If they match, the
    position is returned. If target is less, search continues in left half.
    If target is greater, search continues in right half.

Time Complexity: O(log n) - divides search space in half each iteration
Space Complexity: O(1) for iterative, O(log n) for recursive

Author: [Your Name]
Date: December 2025
"""


def busqueda_binaria(lista_ordenada, isbn_buscado, inicio=0, fin=None):
    """
    Perform binary search for a book by ISBN in a sorted list.
    
    This is the main binary search function that finds a book's position
    in the Sorted Inventory. This function is CRITICAL for the project.
    
    Args:
        lista_ordenada (list): List of books sorted by ISBN (ascending)
        isbn_buscado (str): ISBN to search for
        inicio (int, optional): Starting index. Defaults to 0.
        fin (int, optional): Ending index. Defaults to None (end of list).
        
    Returns:
        int: Position of the book if found, -1 if not found
        
    Example:
        >>> posicion = busqueda_binaria(inventario_ordenado, "978-0-123456-78-9")
        >>> if posicion != -1:
        ...     print(f"Book found at position {posicion}")
        ... else:
        ...     print("Book not found")
    """
    if fin is None:
        fin = len(lista_ordenada) - 1
    
    # Normalize search ISBN
    isbn_buscado = str(isbn_buscado).strip()
    
    # Iterative binary search
    while inicio <= fin:
        # Calculate middle position
        medio = (inicio + fin) // 2
        
        # Get ISBN from the middle element
        libro_medio = lista_ordenada[medio]
        if isinstance(libro_medio, dict):
            isbn_medio = str(libro_medio.get('isbn', '')).strip()
        else:
            isbn_medio = str(getattr(libro_medio, 'isbn', '')).strip()
        
        # Compare ISBNs
        if isbn_medio == isbn_buscado:
            # Found! Return position
            return medio
        elif isbn_medio < isbn_buscado:
            # Target is in right half
            inicio = medio + 1
        else:
            # Target is in left half
            fin = medio - 1
    
    # Not found
    return -1


def busqueda_binaria_recursiva(lista_ordenada, isbn_buscado, inicio=0, fin=None):
    """
    Perform binary search recursively for a book by ISBN.
    
    This is a recursive implementation of binary search, useful for
    understanding the divide-and-conquer approach.
    
    Args:
        lista_ordenada (list): List of books sorted by ISBN (ascending)
        isbn_buscado (str): ISBN to search for
        inicio (int, optional): Starting index. Defaults to 0.
        fin (int, optional): Ending index. Defaults to None (end of list).
        
    Returns:
        int: Position of the book if found, -1 if not found
    """
    if fin is None:
        fin = len(lista_ordenada) - 1
    
    # Base case: search space is empty
    if inicio > fin:
        return -1
    
    # Normalize search ISBN
    isbn_buscado = str(isbn_buscado).strip()
    
    # Calculate middle position
    medio = (inicio + fin) // 2
    
    # Get ISBN from the middle element
    libro_medio = lista_ordenada[medio]
    if isinstance(libro_medio, dict):
        isbn_medio = str(libro_medio.get('isbn', '')).strip()
    else:
        isbn_medio = str(getattr(libro_medio, 'isbn', '')).strip()
    
    # Compare ISBNs
    if isbn_medio == isbn_buscado:
        # Found! Return position
        return medio
    elif isbn_medio < isbn_buscado:
        # Search in right half
        return busqueda_binaria_recursiva(lista_ordenada, isbn_buscado, medio + 1, fin)
    else:
        # Search in left half
        return busqueda_binaria_recursiva(lista_ordenada, isbn_buscado, inicio, medio - 1)


def buscar_libro_por_isbn(lista_ordenada, isbn):
    """
    Search for a book by ISBN and return the book object.
    
    This is a convenience function that performs binary search and
    returns the actual book object instead of just the position.
    
    Args:
        lista_ordenada (list): List of books sorted by ISBN
        isbn (str): ISBN to search for
        
    Returns:
        Book object or dict if found, None if not found
        
    Example:
        >>> libro = buscar_libro_por_isbn(inventario_ordenado, "978-0-123456-78-9")
        >>> if libro:
        ...     print(f"Found: {libro.titulo}")
    """
    posicion = busqueda_binaria(lista_ordenada, isbn)
    
    if posicion != -1:
        return lista_ordenada[posicion]
    
    return None


def verificar_y_asignar_reserva(isbn, inventario_ordenado, cola_reservas, gestor_prestamos=None):
    """
    CRITICAL FUNCTION: Verify if a returned book has pending reservations.
    
    This function is the CRITICAL requirement of the project. When a book
    is returned, this function MUST be called to:
    1. Use binary search to find the book in the sorted inventory
    2. Check if there are reservations in the queue for this book
    3. If reservations exist, assign the book to the first user in line (FIFO)
    4. Process the automatic loan if possible
    
    PROJECT REQUIREMENT:
        Binary search result must be used to verify pending reservations.
        If reservations exist, assign to first person in queue by priority.
    
    Args:
        isbn (str): ISBN of the returned book
        inventario_ordenado (list): Sorted inventory list
        cola_reservas: Cola (Queue) object with reservations
        gestor_prestamos: Optional loan manager to process automatic assignment
        
    Returns:
        dict: Result information with keys:
              - 'libro_encontrado' (bool): If book was found
              - 'posicion' (int): Position in sorted inventory (-1 if not found)
              - 'tiene_reservas' (bool): If book has pending reservations
              - 'usuario_asignado' (str or None): User ID who got the book
              - 'reserva_procesada' (dict or None): Processed reservation details
              
    Example:
        >>> resultado = verificar_y_asignar_reserva(
        ...     "978-0-123456-78-9",
        ...     inventario_ordenado,
        ...     cola_reservas,
        ...     gestor_prestamos
        ... )
        >>> if resultado['usuario_asignado']:
        ...     print(f"Book assigned to user {resultado['usuario_asignado']}")
    """
    # Step 1: Use BINARY SEARCH to find the book (CRITICAL REQUIREMENT)
    posicion = busqueda_binaria(inventario_ordenado, isbn)
    
    resultado = {
        'libro_encontrado': posicion != -1,
        'posicion': posicion,
        'tiene_reservas': False,
        'usuario_asignado': None,
        'reserva_procesada': None
    }
    
    # If book not found, return early
    if posicion == -1:
        return resultado
    
    # Step 2: Check if there are pending reservations for this book
    siguiente_reserva = cola_reservas.obtener_siguiente_usuario(isbn)
    
    if siguiente_reserva is None:
        # No reservations pending
        return resultado
    
    # Step 3: There are reservations! Dequeue the first one (FIFO priority)
    resultado['tiene_reservas'] = True
    reserva = cola_reservas.desencolar()
    
    if reserva:
        resultado['usuario_asignado'] = reserva['id_usuario']
        resultado['reserva_procesada'] = reserva
        
        # Step 4: If loan manager is provided, process automatic loan
        if gestor_prestamos:
            try:
                # Process the loan automatically for the reserved user
                exito = gestor_prestamos.procesar_prestamo_automatico(
                    reserva['id_usuario'],
                    isbn
                )
                resultado['prestamo_procesado'] = exito
            except Exception as e:
                resultado['error'] = str(e)
    
    return resultado


def contar_comparaciones_binaria(lista_ordenada, isbn_buscado):
    """
    Count how many comparisons binary search makes.
    
    This utility function demonstrates the efficiency of binary search
    by counting comparisons.
    
    Args:
        lista_ordenada (list): Sorted list of books
        isbn_buscado (str): ISBN to search for
        
    Returns:
        dict: Contains 'posicion', 'comparaciones', and 'encontrado'
        
    Example:
        >>> resultado = contar_comparaciones_binaria(inventario, "978-0-123456-78-9")
        >>> print(f"Found in {resultado['comparaciones']} comparisons")
    """
    inicio = 0
    fin = len(lista_ordenada) - 1
    isbn_buscado = str(isbn_buscado).strip()
    comparaciones = 0
    
    while inicio <= fin:
        comparaciones += 1
        medio = (inicio + fin) // 2
        
        libro_medio = lista_ordenada[medio]
        if isinstance(libro_medio, dict):
            isbn_medio = str(libro_medio.get('isbn', '')).strip()
        else:
            isbn_medio = str(getattr(libro_medio, 'isbn', '')).strip()
        
        if isbn_medio == isbn_buscado:
            return {
                'posicion': medio,
                'comparaciones': comparaciones,
                'encontrado': True
            }
        elif isbn_medio < isbn_buscado:
            inicio = medio + 1
        else:
            fin = medio - 1
    
    return {
        'posicion': -1,
        'comparaciones': comparaciones,
        'encontrado': False
    }


def verificar_lista_ordenada(lista_libros):
    """
    Verify that a list is correctly sorted by ISBN for binary search.
    
    Binary search requires a sorted list. This function validates that
    the list is properly sorted in ascending order by ISBN.
    
    Args:
        lista_libros (list): List to verify
        
    Returns:
        dict: Contains 'ordenada' (bool), 'mensaje' (str), and 'error_posicion' (int)
        
    Example:
        >>> resultado = verificar_lista_ordenada(inventario_ordenado)
        >>> if not resultado['ordenada']:
        ...     print(f"List not sorted! Error at position {resultado['error_posicion']}")
    """
    if len(lista_libros) <= 1:
        return {'ordenada': True, 'mensaje': 'List has 0 or 1 elements', 'error_posicion': -1}
    
    for i in range(len(lista_libros) - 1):
        if isinstance(lista_libros[i], dict):
            isbn_actual = str(lista_libros[i].get('isbn', '')).strip()
            isbn_siguiente = str(lista_libros[i + 1].get('isbn', '')).strip()
        else:
            isbn_actual = str(getattr(lista_libros[i], 'isbn', '')).strip()
            isbn_siguiente = str(getattr(lista_libros[i + 1], 'isbn', '')).strip()
        
        if isbn_actual > isbn_siguiente:
            return {
                'ordenada': False,
                'mensaje': f'List not sorted: ISBN at position {i} > ISBN at position {i+1}',
                'error_posicion': i
            }
    
    return {'ordenada': True, 'mensaje': 'List is correctly sorted', 'error_posicion': -1}


def demostrar_busqueda_binaria(lista_ordenada, isbn_buscado):
    """
    Demonstrate the binary search process step by step.
    
    This function shows how the algorithm divides the search space in half
    with each iteration, making it much more efficient than linear search.
    
    Args:
        lista_ordenada (list): Sorted list of books
        isbn_buscado (str): ISBN to search for
        
    Note:
        This function prints to console for educational purposes.
    """
    print("=== Binary Search Demonstration ===")
    print(f"Searching for ISBN: {isbn_buscado}")
    print(f"Total elements in list: {len(lista_ordenada)}")
    print()
    
    inicio = 0
    fin = len(lista_ordenada) - 1
    isbn_buscado = str(isbn_buscado).strip()
    paso = 1
    
    while inicio <= fin:
        medio = (inicio + fin) // 2
        
        libro_medio = lista_ordenada[medio]
        if isinstance(libro_medio, dict):
            isbn_medio = str(libro_medio.get('isbn', '')).strip()
        else:
            isbn_medio = str(getattr(libro_medio, 'isbn', '')).strip()
        
        print(f"Step {paso}:")
        print(f"  Search range: [{inicio}, {fin}] (size: {fin - inicio + 1})")
        print(f"  Middle position: {medio}")
        print(f"  Middle ISBN: {isbn_medio}")
        print(f"  Target ISBN: {isbn_buscado}")
        
        if isbn_medio == isbn_buscado:
            print(f"  ✓ MATCH FOUND at position {medio}!")
            print()
            print("=== Search Complete ===")
            print(f"Total steps: {paso}")
            print(f"Efficiency: Checked {paso} elements out of {len(lista_ordenada)}")
            return medio
        elif isbn_medio < isbn_buscado:
            print(f"  Target is greater → Search RIGHT half")
            inicio = medio + 1
        else:
            print(f"  Target is smaller → Search LEFT half")
            fin = medio - 1
        
        print()
        paso += 1
    
    print("=== Search Complete ===")
    print(f"ISBN not found after {paso - 1} steps")
    return -1


def buscar_rango_isbn(lista_ordenada, isbn_inicio, isbn_fin):
    """
    Find all books with ISBNs in a given range using binary search.
    
    This function uses binary search to efficiently find the start and end
    positions of a range, then returns all books in that range.
    
    Args:
        lista_ordenada (list): Sorted list of books
        isbn_inicio (str): Starting ISBN (inclusive)
        isbn_fin (str): Ending ISBN (inclusive)
        
    Returns:
        list: All books with ISBNs in the specified range
    """
    # Find starting position
    pos_inicio = 0
    for i, libro in enumerate(lista_ordenada):
        if isinstance(libro, dict):
            isbn = str(libro.get('isbn', '')).strip()
        else:
            isbn = str(getattr(libro, 'isbn', '')).strip()
        
        if isbn >= isbn_inicio:
            pos_inicio = i
            break
    
    # Find ending position
    pos_fin = len(lista_ordenada) - 1
    for i in range(len(lista_ordenada) - 1, -1, -1):
        libro = lista_ordenada[i]
        if isinstance(libro, dict):
            isbn = str(libro.get('isbn', '')).strip()
        else:
            isbn = str(getattr(libro, 'isbn', '')).strip()
        
        if isbn <= isbn_fin:
            pos_fin = i
            break
    
    # Return the range
    if pos_inicio <= pos_fin:
        return lista_ordenada[pos_inicio:pos_fin + 1]
    
    return []