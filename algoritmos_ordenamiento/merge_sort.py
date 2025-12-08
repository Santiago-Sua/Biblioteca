"""
Merge Sort Algorithm - Library Management System

This module implements the Merge Sort algorithm used to generate global
inventory reports sorted by value (COP). This divide-and-conquer recursive
algorithm provides consistent O(n log n) performance.

The Merge Sort is ideal for generating reports because:
1. It has guaranteed O(n log n) performance in all cases
2. It's stable (maintains relative order of equal elements)
3. It works well with large datasets
4. It's efficient for sorting by different criteria

Algorithm Explanation:
    The algorithm works by recursively dividing the list into smaller sublists
    until each sublist has one element. Then it merges the sublists back together
    in sorted order, comparing elements from each sublist.

Time Complexity: O(n log n) in all cases (best, average, worst)
Space Complexity: O(n) - requires additional space for merging

Author: [Your Name]
Date: December 2025
"""


def ordenamiento_mezcla(lista_libros, clave='valor', reverso=False):
    """
    Sort a list of books using Merge Sort algorithm.
    
    This is the main function that initiates the merge sort process.
    It creates a copy of the list to avoid modifying the original.
    
    Args:
        lista_libros (list): List of book objects or dictionaries to sort
        clave (str, optional): Attribute/key to sort by. Defaults to 'valor'.
        reverso (bool, optional): If True, sort in descending order. Defaults to False.
        
    Returns:
        list: New sorted list (original list is not modified)
        
    Example:
        >>> libros = [libro1, libro2, libro3]
        >>> libros_ordenados = ordenamiento_mezcla(libros, clave='valor')
        >>> # libros_ordenados is sorted by value, libros remains unchanged
    """
    # Create a copy to avoid modifying the original list
    lista_copia = lista_libros.copy()
    
    # Call the recursive merge sort function
    _merge_sort_recursivo(lista_copia, 0, len(lista_copia) - 1, clave, reverso)
    
    return lista_copia


def _merge_sort_recursivo(lista, inicio, fin, clave, reverso):
    """
    Recursive helper function for merge sort.
    
    This function implements the divide-and-conquer approach by recursively
    splitting the list into halves and then merging them back in sorted order.
    
    Args:
        lista (list): List to sort (modified in-place)
        inicio (int): Starting index of the portion to sort
        fin (int): Ending index of the portion to sort
        clave (str): Attribute/key to sort by
        reverso (bool): If True, sort in descending order
    """
    # Base case: if the portion has one or zero elements, it's already sorted
    if inicio >= fin:
        return
    
    # Divide: find the middle point
    medio = (inicio + fin) // 2
    
    # Conquer: recursively sort both halves
    _merge_sort_recursivo(lista, inicio, medio, clave, reverso)
    _merge_sort_recursivo(lista, medio + 1, fin, clave, reverso)
    
    # Combine: merge the sorted halves
    _mezclar(lista, inicio, medio, fin, clave, reverso)


def _mezclar(lista, inicio, medio, fin, clave, reverso):
    """
    Merge two sorted portions of a list into one sorted portion.
    
    This is the core merging operation that combines two sorted sublists
    into a single sorted sublist.
    
    Args:
        lista (list): List containing the portions to merge
        inicio (int): Starting index of first portion
        medio (int): Ending index of first portion (start of second is medio+1)
        fin (int): Ending index of second portion
        clave (str): Attribute/key to sort by
        reverso (bool): If True, sort in descending order
    """
    # Create temporary copies of both portions
    izquierda = lista[inicio:medio + 1]
    derecha = lista[medio + 1:fin + 1]
    
    # Initialize pointers for merging
    i = 0  # Pointer for left portion
    j = 0  # Pointer for right portion
    k = inicio  # Pointer for merged result in original list
    
    # Merge the two portions by comparing elements
    while i < len(izquierda) and j < len(derecha):
        # Get values to compare
        valor_izq = _obtener_valor(izquierda[i], clave)
        valor_der = _obtener_valor(derecha[j], clave)
        
        # Determine which element to place next based on sort order
        if reverso:
            # Descending order: place larger element first
            if valor_izq >= valor_der:
                lista[k] = izquierda[i]
                i += 1
            else:
                lista[k] = derecha[j]
                j += 1
        else:
            # Ascending order: place smaller element first
            if valor_izq <= valor_der:
                lista[k] = izquierda[i]
                i += 1
            else:
                lista[k] = derecha[j]
                j += 1
        
        k += 1
    
    # Copy any remaining elements from left portion
    while i < len(izquierda):
        lista[k] = izquierda[i]
        i += 1
        k += 1
    
    # Copy any remaining elements from right portion
    while j < len(derecha):
        lista[k] = derecha[j]
        j += 1
        k += 1


def _obtener_valor(elemento, clave):
    """
    Extract the value of a key from an element.
    
    Helper function to get the comparison value from either a dictionary
    or an object with attributes.
    
    Args:
        elemento: Book object or dictionary
        clave (str): Attribute/key name
        
    Returns:
        Comparable value for sorting
    """
    if isinstance(elemento, dict):
        return elemento.get(clave, 0)
    else:
        return getattr(elemento, clave, 0)


def merge_sort_por_atributo(lista_libros, atributos, orden_reverso=None):
    """
    Sort books by multiple attributes in priority order.
    
    This function allows sorting by multiple criteria, where the first
    attribute has highest priority, then second, etc.
    
    Args:
        lista_libros (list): List of books to sort
        atributos (list): List of attribute names in priority order
        orden_reverso (list, optional): List of booleans for each attribute.
                                       True for descending, False for ascending.
                                       Defaults to all False.
        
    Returns:
        list: New sorted list
        
    Example:
        >>> # Sort by genre (asc), then by value (desc)
        >>> libros_ordenados = merge_sort_por_atributo(
        ...     libros, 
        ...     atributos=['genero', 'valor'],
        ...     orden_reverso=[False, True]
        ... )
    """
    if orden_reverso is None:
        orden_reverso = [False] * len(atributos)
    
    # Start with a copy of the list
    resultado = lista_libros.copy()
    
    # Sort by each attribute in reverse priority order
    # (last attribute first, so primary attribute has final say)
    for i in range(len(atributos) - 1, -1, -1):
        resultado = ordenamiento_mezcla(resultado, atributos[i], orden_reverso[i])
    
    return resultado


def generar_reporte_ordenado(lista_libros, clave='valor', reverso=True, 
                             formato='dict', incluir_indices=False):
    """
    Generate a sorted report of the inventory.
    
    This is the main function used for generating global inventory reports
    sorted by value (COP) as required by the project.
    
    Args:
        lista_libros (list): List of books to include in report
        clave (str, optional): Attribute to sort by. Defaults to 'valor'.
        reverso (bool, optional): Sort descending. Defaults to True (highest value first).
        formato (str, optional): Output format ('dict' or 'objeto'). Defaults to 'dict'.
        incluir_indices (bool, optional): Include position index. Defaults to False.
        
    Returns:
        list: Sorted list ready for report generation
        
    Example:
        >>> reporte = generar_reporte_ordenado(inventario, clave='valor', reverso=True)
        >>> # reporte contains books sorted by value (highest to lowest)
    """
    # Sort the books
    libros_ordenados = ordenamiento_mezcla(lista_libros, clave, reverso)
    
    # Convert to dictionary format if requested
    if formato == 'dict':
        resultado = []
        for idx, libro in enumerate(libros_ordenados):
            if isinstance(libro, dict):
                libro_dict = libro.copy()
            else:
                libro_dict = libro.to_dict()
            
            if incluir_indices:
                libro_dict['posicion'] = idx + 1
            
            resultado.append(libro_dict)
        
        return resultado
    
    return libros_ordenados


def demostrar_merge_sort(lista_libros, clave='valor', nivel=0):
    """
    Demonstrate the Merge Sort algorithm step by step with visualization.
    
    This recursive function prints the division and merging process for
    educational purposes, showing how the algorithm works.
    
    Args:
        lista_libros (list): List of books to sort
        clave (str, optional): Attribute to sort by. Defaults to 'valor'.
        nivel (int, optional): Recursion depth (for indentation). Defaults to 0.
        
    Returns:
        list: Sorted list
        
    Note:
        This function prints to console and is intended for demonstration only.
    """
    indent = "  " * nivel
    
    # Get values for display
    valores = [_obtener_valor(libro, clave) for libro in lista_libros]
    
    print(f"{indent}[Level {nivel}] Sorting: {valores}")
    
    # Base case
    if len(lista_libros) <= 1:
        print(f"{indent}[Level {nivel}] Base case reached (single element)")
        return lista_libros.copy()
    
    # Divide
    medio = len(lista_libros) // 2
    izquierda = lista_libros[:medio]
    derecha = lista_libros[medio:]
    
    print(f"{indent}[Level {nivel}] Dividing into:")
    print(f"{indent}  Left: {[_obtener_valor(l, clave) for l in izquierda]}")
    print(f"{indent}  Right: {[_obtener_valor(l, clave) for l in derecha]}")
    
    # Conquer (recursive calls)
    izquierda_ordenada = demostrar_merge_sort(izquierda, clave, nivel + 1)
    derecha_ordenada = demostrar_merge_sort(derecha, clave, nivel + 1)
    
    # Combine (merge)
    resultado = []
    i = j = 0
    
    while i < len(izquierda_ordenada) and j < len(derecha_ordenada):
        val_izq = _obtener_valor(izquierda_ordenada[i], clave)
        val_der = _obtener_valor(derecha_ordenada[j], clave)
        
        if val_izq <= val_der:
            resultado.append(izquierda_ordenada[i])
            i += 1
        else:
            resultado.append(derecha_ordenada[j])
            j += 1
    
    resultado.extend(izquierda_ordenada[i:])
    resultado.extend(derecha_ordenada[j:])
    
    valores_resultado = [_obtener_valor(libro, clave) for libro in resultado]
    print(f"{indent}[Level {nivel}] Merged result: {valores_resultado}")
    
    return resultado